document.addEventListener("DOMContentLoaded", function () {
    const clientList = document.getElementById("clientList");
    const jobList = document.getElementById("jobList");
    const chatMessages = document.getElementById("chatMessages");
    const chatForm = document.getElementById("chatForm");
    const messageInput = document.getElementById("messageInput");

    let selectedClientId = null;
    let selectedJobId = null;
    let isAdmin = document.body.dataset.isAdmin === "true";  // Detect if Admin
    let isClientPortal = document.body.dataset.pageType === "client_portal";  // Detect Client Portal

    // ✅ Admin: Select Client & Fetch Their Jobs
    if (isAdmin && clientList) {
        clientList.addEventListener("click", function (event) {
            if (event.target.classList.contains("client-link")) {
                event.preventDefault();
                selectedClientId = event.target.dataset.clientId;
                jobList.innerHTML = "<li>Loading jobs...</li>";  // ✅ Show loading state
                chatMessages.innerHTML = "";

                console.log("📌 Admin selected client:", selectedClientId);

                fetch(`/chat/?client_id=${selectedClientId}`, {
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log("📄 Jobs Loaded:", data.jobs);  // Debug Log ✅

                        jobList.innerHTML = "";  // ✅ Clear list after jobs are fetched

                        if (data.jobs.length === 0) {
                            jobList.innerHTML = "<li>No jobs found for this client.</li>";
                        } else {
                            data.jobs.forEach(job => {
                                let jobItem = document.createElement("li");
                                jobItem.innerHTML = `<a href="#" class="job-link" data-job-id="${job.id}">${job.title}</a>`;
                                jobList.appendChild(jobItem);
                            });
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching jobs:", error);
                        jobList.innerHTML = "<li>Error loading jobs. Please try again.</li>";
                    });
            }
        });
    }

    // ✅ Auto-load jobs for Clients (Clients don't need to select themselves)
    if (isClientPortal) {
        fetch(`/chat/?auto_load_jobs=true`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then(response => response.json())
            .then(data => {
                jobList.innerHTML = "";
                data.jobs.forEach(job => {
                    let jobItem = document.createElement("li");
                    jobItem.innerHTML = `<a href="#" class="job-link" data-job-id="${job.id}">${job.title}</a>`;
                    jobList.appendChild(jobItem);
                });
            })
            .catch(error => console.error("Error fetching jobs:", error));
    }

    // ✅ FIX: Prevent Page Scroll on Job Click & Load Messages
    if (jobList) {
        jobList.addEventListener("click", function (event) {
            if (event.target.classList.contains("job-link")) {
                event.preventDefault();
                selectedJobId = event.target.dataset.jobId;
                chatMessages.innerHTML = "<p>Loading messages...</p>";  // ✅ Show loading state

                console.log("📌 Selected job:", selectedJobId);

                fetch(`/chat/?job_id=${selectedJobId}`, {
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                })
                    .then(response => response.json())
                    .then(data => {
                        chatMessages.innerHTML = "";
                        data.messages.forEach(msg => {
                            let newMessage = document.createElement("div");
                            newMessage.classList.add("message");
                            newMessage.innerHTML = `
                            <strong>${msg.sender__username}:</strong> ${msg.text} 
                            <span class="timestamp">${formatTimestamp(msg.sent_at)}</span>`;
                            chatMessages.appendChild(newMessage);
                        });
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    })
                    .catch(error => {
                        console.error("Error fetching messages:", error);
                        chatMessages.innerHTML = "<p>Error loading messages.</p>";
                    });
            }
        });
    }

    // ✅ Send Message via AJAX (No Page Reload)
    if (chatForm) {
        chatForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let messageText = messageInput.value.trim();
            if (!messageText || !selectedJobId) {
                alert("Please select a job before sending a message.");
                return;
            }

            let formData = new FormData(chatForm);
            formData.append("job_id", selectedJobId);

            let url = isAdmin
                ? `/chat/${selectedClientId}/${selectedJobId}/`
                : `/chat/user/${selectedJobId}/`;

            console.log("📡 Sending Message to:", url);
            console.log("📩 Message:", messageText);
            console.log("📌 Selected Job ID:", selectedJobId);

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let newMessage = document.createElement("div");
                        newMessage.classList.add("message");
                        newMessage.innerHTML = `
                        <strong>${data.sender}:</strong> ${data.text} 
                        <span class="timestamp">${formatTimestamp(data.timestamp)}</span>`;
                        chatMessages.appendChild(newMessage);

                        messageInput.value = "";
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                    } else {
                        console.error("Error: ", data.error);
                    }
                })
                .catch(error => console.error("Error sending message:", error));
        });
    }

    function formatTimestamp(timestamp) {
        let date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
});
