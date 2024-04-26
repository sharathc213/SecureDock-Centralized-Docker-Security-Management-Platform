$(document).ready(function() {
    // Function to get CSRF token from cookies
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
    var csrftoken = getCookie('csrftoken');

    // Function to toggle button visibility
    function toggleButtons(enableButtonVisible) {
        if (enableButtonVisible) {
            $('#start-task-btn').show();
            $('#stop-task-btn').hide();
            $('.copybutton').html("");

        } else {
            $('#start-task-btn').hide();
            $('#stop-task-btn').show();
             $('.newclient').html("");
        }
    }

    // Initial visibility setup
    toggleButtons(true); // Assuming the task is initially disabled

    $('#start-task-btn').click(function() {
        $.ajax({
            url: '/client/enable/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
            if(response.message){
                var but=`
                            <button onclick="copyToClipboard()"  class="btn btn-flex explore-btn-outline w-100 flex-stack px-4 mb-4">
                                    <!--begin::Info-->
                                    <div class="d-flex align-items-center me-1">
                                        
                                        <div class="d-flex flex-column align-items-start">
                                            <h3 class="text-gray-800 fs-6 fw-bold mb-0">Click Here to copy Client Instalation Comment</h3>
                                            
                                        </div>
                                    </div>
                                <div id="textToCopy" style="display: none;">curl http://${response.ip}:${response.port}/download/setup/?token=${response.token} | bash</div>
                                    <!--end::Label-->
                                </button>`
         $('.copybutton').html(but);
                    Message('Lissoner Started', 'Success', 'success'); 
                    toggleButtons(false); // Disable button clicked, so hide it and show enable button
                }else{
                    Message('Some thing Wrong', 'Error', 'error');
                }
            }
        });
    });

    $('#stop-task-btn').click(function() {
        $.ajax({
            url: '/client/disable/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                if(response.message){
                    Message('Lissoner Stoped', 'Success', 'success'); 
                    toggleButtons(true); // Disable button clicked, so hide it and show enable button
                }else{
                     Message('Some thing Wrong', 'Error', 'error');
                }
         
              
            }
        });
    });


        // Function to check button status
    function checkButtonStatus() {
        $.ajax({
            url: '/dashboard/check-button-status/',
            type: 'POST',
             headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                toggleButtons(response.status);
            }
        });
    }

    // Initial check for button status
    checkButtonStatus();
countClient()
    // Periodically check for button status
    setInterval(checkButtonStatus, 10000); 
    setInterval(countClient, 10000); 

});
