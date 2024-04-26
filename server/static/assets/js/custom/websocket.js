var socket = new WebSocket('ws://localhost:8000/ws/output/')
socket.onmessage=function(event){
    var message=event.data;
if(JSON.parse(message).data=='data'){
var template = `
    <div class="pt-15 mb-0">
        <div class="d-flex flex-stack mb-5">
            <h3 class="fw-bolder text-dark me-2 mb-0">New Clients Added</h3>
        </div>
        <div class="mb-0">
            <button class="btn btn-flex explore-btn-outline w-100 flex-stack active px-4 mb-4">
                <div class="d-flex align-items-center me-1">
                    <div class="d-flex flex-column align-items-start">
                        <h3 class="text-gray-800 fs-6 fw-bold mb-0">${JSON.parse(message).ip}</h3>
                        <!-- <div class="text-gray-400 fs-7 fw-bold">HTML, CSS, JS, Bootstrap 5</div> -->
                    </div>
                </div>
            </button>
        </div>
    </div>
`;


$('.newclient').html(template);
$('#stop-task-btn').hide();
$('.copybutton').html("");
            $('#start-task-btn').show();
            fetchClients()
Message('Mew Client is added', 'Success', 'success'); 
}else if(JSON.parse(message).data=='info'){

    var template = `
    <div class="pt-15 mb-0">
        <div class="d-flex flex-stack mb-5">
            <h3 class="fw-bolder text-dark me-2 mb-0">Clients Token Updated</h3>
        </div>
        <div class="mb-0">
            <button class="btn btn-flex explore-btn-outline w-100 flex-stack active px-4 mb-4">
                <div class="d-flex align-items-center me-1">
                    <div class="d-flex flex-column align-items-start">
                        <h3 class="text-gray-800 fs-6 fw-bold mb-0">${JSON.parse(message).ip}</h3>
                        <!-- <div class="text-gray-400 fs-7 fw-bold">HTML, CSS, JS, Bootstrap 5</div> -->
                    </div>
                </div>
            </button>
        </div>
    </div>
`;

$('.newclient').html(template);
$('#stop-task-btn').hide();
$('.copybutton').html("");
            $('#start-task-btn').show();
            fetchClients()
  Message('Token Updated', 'Info', 'info');   
}else{
  Message('Client Added error', 'Error', 'error');    
}
}