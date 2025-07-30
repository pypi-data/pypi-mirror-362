//Utility function for reporting task values from arbitrary html inputs
function toppyt_notify(element, sync, name, value) {
    var cur = element;
    while(!cur.hasAttribute('data-toppyt-task')) { //Search wrapping task element
        cur = cur.parentElement;
    }
    if(name === undefined) {
        name = element.name
    }
    if(value === undefined) {
        if(element.type === 'checkbox') {
            value = element.checked;
        } else {
            value = element.value;
        }
    }
    if(cur.updates === undefined) {
        cur.updates = {};
    }
    cur.updates[name] = value;

    if(sync) {
        document.querySelector('toppyt-session').syncTasks();
    }
}
//Uploads are handled with a separate PUT request
function toppyt_notify_file(element, upload_url, sync) {
    fetch(upload_url, {
        method: 'PUT',
        body: element.files[0]
    })
    .then(response => response.json())
    .then(result => {
        const value = {
            'name': element.files[0].name,
            'type': element.files[0].type,
            'id':result['id']
        };
        toppyt_notify(element, sync, undefined, value);
    });
}

function toppyt_value(element) {
    if(element.updates === undefined || Object.keys(element.updates).length == 0) {
        return null;
    }
    const value = {};
    for(let key of Object.keys(element.updates)) {
        const path = key.split("-");
        let container = value;
        //Walk and create containers if necessary
        for(let step of path.splice(0,path.length - 1)) {
            if(!(step in container)) {
                container[step] = {};    
            }
            container = container[step];
        }
        container[path[0]] = element.updates[key];
    }
    return value['v'];
}

class ToppytSession extends HTMLElement {
    constructor() {
        super();
        this.sessionid = this.getAttribute("session-id");
        this.path = this.getAttribute("start-path");
        if(this.path != document.location.pathname) {
            history.pushState(null,'',this.path);
        }
        this.socket = null;
        window.onpopstate = e => this.onPathChange();

        //TEMPORARY: Always connect websocket.
        //When it is needed should be determined by the tasks
        this.connectSocket();
    }
    onPathChange() {
        let newpath = document.location.pathname;
        if(newpath != this.path) {
            this.path = newpath;
            this.syncTasks(true);
        }
    }
    connectSocket() {
        const use_wss = location.protocol.startsWith('https');
        const url = `${use_wss ? 'wss': 'ws'}://${document.location.hostname}:${document.location.port}/`;
        this.socket = new WebSocket(url);
        this.socket.addEventListener('open', e => this.onConnect());
        this.socket.addEventListener('message', message => this.onMessage(message));
        this.socket.addEventListener('close', e => this.onDisconnect());
    }
    onConnect() {
        this.socket.send(JSON.stringify({'session-id':this.sessionid}));
    }
    onMessage(message) {
        this.updatePage(JSON.parse(message.data));
    }
    onDisconnect() {
        this.socket = null;
    }
    syncTasks(syncpath = false) {
        const body = {};
        
        if(syncpath) {
            body['path'] = this.path;
        }
        //Temporary: synchronize all tasks
        //Should check better which tasks/editors have been edited
        for(let element of document.querySelectorAll('[data-toppyt-task]')) {
            let value = toppyt_value(element);
            if(value !== null) {
                body[element.getAttribute("data-toppyt-task")] = value;
            }
        }
        if (this.socket != null) {
            //If a websocket connection is available, use it to send the event.
            this.socket.send(JSON.stringify(body));
        } else {
            //Synchronize using a post request
            body['session-id'] = this.sessionid;
            window.fetch(window.location, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(body)
            })
            .then(response => response.json())
            .then(updates => this.updatePage(updates));
        }
    }
    updatePage(updates) {
        if('path' in updates) {
            this.path = updates['path'];
            history.pushState(null,'',updates['path']);
        }
        if('cookies' in updates) {
            for(let cookie of updates['cookies']) {
                document.cookie = cookie[0] + '=' + cookie[1] + (cookie[2] === null ? '' : ';Max-Age='+cookie[2]) + '; Path=/; SameSite=Strict';
            }
        }
        if('error' in updates && (updates['error'] == 'unknown-session' || updates['error'] == 'no-session-id')) {
            document.body.innerHTML = 'Failed to load session. Refreshing page...';
            window.location = window.location;
        }
        
        const wrapper = document.createElement('div');
        for(let task of document.querySelectorAll('[data-toppyt-task]')) {
            const taskid = task.getAttribute("data-toppyt-task");
            
            if(taskid in updates) {
                wrapper.innerHTML = updates[taskid];
            
                //Allow custom replacement by editors
                //Only if 1) editor is direct descendent of task, 2) task is not replaced by another task, and 3) editor supports replacement.
                if(task.children.length == 1 && task.children[0].toppyt_replace !== undefined && wrapper.firstChild.getAttribute('data-toppyt-taskid') == taskid) {
                    task.children[0].toppyt_replace(wrapper.firstChild.children[0]);
                    continue;
                } 

                //Attach keygroup handlers before replacing the element
                for(const keygroup of wrapper.querySelectorAll('[data-toppyt-keygroup]')) {
                    keygroup.addEventListener('keyup',((target) => (e) => {
                        if (e.keyCode == 13 || e.keyCode == 27 ) { //Enter or escape key
                            for(const el of target.getElementsByClassName(e.keyCode == 13 ? 'toppyt-enter': 'toppyt-escape')) {
                                toppyt_notify(el,false);
                            }
                            document.querySelector('toppyt-session').syncTasks();
                        }
                    })(keygroup));
                }
                task.replaceWith(wrapper.firstElementChild);
            } 
        }
    }
}
customElements.define('toppyt-session',ToppytSession);