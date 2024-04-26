 function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Check if the cookie contains the csrf token
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // CSRF token
    


    function deleteClient(clientId) {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/client/deleteclient/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: {
                id: clientId
            },
            success: function(response) {
           if(response.message){
        
                    Message('Delete Successfull', 'Success', 'success'); 
               fetchClients()
                    countClient()
                }else{
                    Message('Some thing Wrong', 'Error', 'error');
                }
                // Refresh the client list after deletion

            },
            error: function(xhr, status, error) {
                 Message('Some thing Wrong', 'Error', 'error');
            }
        });
    }


    // Function to fetch clients via AJAX
    function fetchClients() {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/client/listclient/',
            type: 'Post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                // Handle successful response
            
                displayClients(response.clients);
            },
            error: function(xhr, errmsg, err) {
                // Handle error
                 Message(xhr.status + ": " + xhr.responseText, 'Error', 'error');
             
            }
        });
    }

    // Function to display clients on the webpage
    function displayClients(clients) {
        var clientList = $('.listclients'); 
        // Clear existing content
        clientList.empty();

        // Append each client to the list
        clients.forEach(function(client) {


var clientItem = `
    <tr>
        <td class="ps-0">
            <div class="symbol symbol-55px me-2 mt-1">
                ${client.status === 'online' ? 
                    `<button disabled class="btn btn-icon btn-light-success fw-bolder pulse pulse-success" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end" id="kt_activities_toggle">
                        <span class="position-absolute fs-6">Online</span>
                        <span class="pulse-ring"></span>
                    </button>` :
                    `<button disabled class="btn btn-icon btn-light-danger fw-bolder pulse pulse-danger" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end" id="kt_activities_toggle">
                        <span class="position-absolute fs-6">Offline</span>
                        <span class="pulse-ring"></span>
                    </button>`
                }
            </div>
        </td>
        <td class="ps-0">
            <span class="text-dark fw-bolder text-hover-primary fs-6">${client.ip_address}</span>
        </td>
        <td class="text-end pe-0">
            <button class="btn btn-icon btn-danger btn-sm delete-btn" onclick="deleteClient(${client.id})">
                <i class="fab fa fa-trash"></i>
            </button>
        </td>
        <td class="text-end pe-0">
            <a href="dashboard/scan-client/?id=${client.id}" class="btn btn-icon btn-bg-light btn-active-primary btn-sm">
                <!--begin::Svg Icon | path: icons/duotone/Navigation/Arrow-right.svg-->
                <span class="svg-icon svg-icon-4">
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1">
                        <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                            <polygon points="0 0 24 0 24 24 0 24" />
                            <rect fill="#000000" opacity="0.5" transform="translate(12.000000, 12.000000) rotate(-90.000000) translate(-12.000000, -12.000000)" x="11" y="5" width="2" height="14" rx="1" />
                            <path d="M9.70710318,15.7071045 C9.31657888,16.0976288 8.68341391,16.0976288 8.29288961,15.7071045 C7.90236532,15.3165802 7.90236532,14.6834152 8.29288961,14.2928909 L14.2928896,8.29289093 C14.6714686,7.914312 15.281055,7.90106637 15.675721,8.26284357 L21.675721,13.7628436 C22.08284,14.136036 22.1103429,14.7686034 21.7371505,15.1757223 C21.3639581,15.5828413 20.7313908,15.6103443 20.3242718,15.2371519 L15.0300721,10.3841355 L9.70710318,15.7071045 Z" fill="#000000" fill-rule="nonzero" transform="translate(14.999999, 11.999997) scale(1, -1) rotate(90.000000) translate(-14.999999, -11.999997)" />
                    </svg>
                </span>
                <!--end::Svg Icon-->
            </a>
        </td>
    </tr>`;



            clientList.append(clientItem);
        });
    }

    fetchClients();
function copyToClipboard() {
  // Get the text content to copy
  var text = document.getElementById("textToCopy").innerText;
  
  // Create a temporary textarea element
  var tempTextarea = document.createElement("textarea");
  
  // Set the text content of the textarea
  tempTextarea.value = text;
  
  // Append the textarea to the body
  document.body.appendChild(tempTextarea);
  
  // Select the text inside the textarea
  tempTextarea.select();
  
  // Execute the copy command
  document.execCommand("copy");
  
  // Remove the temporary textarea
  document.body.removeChild(tempTextarea);
  
  // Alert the user that the text has been copied
  Message('Instalation Script Copied', 'Info', 'info');
}



    function countClient() {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/client/countclient/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
     
            success: function(response) {
          
            $('.all').html(response.total_client);
            $('.online').html(response.online_client);
            $('.offline').html(response.offline_client);
                // Refresh the client list after deletion;

            },
            error: function(xhr, status, error) {
                 Message('Some thing Wrong', 'Error', 'error');
            }
        });
    }