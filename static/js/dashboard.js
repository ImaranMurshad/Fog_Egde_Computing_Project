const total = Number(document.querySelector(".total-card h2")?.textContent || 0);
const critical = Number(document.querySelector(".critical-card h2")?.textContent || 0);
const high = Number(document.querySelector(".high-card h2")?.textContent || 0);
const medium = Number(document.querySelector(".medium-card h2")?.textContent || 0);

// Bar Chart
new Chart(document.getElementById("alertChart"), {

    type: "bar",

    data: {

        labels: ["Critical", "High", "Medium"],

        datasets: [{

            label: "Alerts",

            data: [critical, high, medium]

        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: false

            }

        }

    }

});

// Doughnut Chart
new Chart(document.getElementById("statusChart"), {

    type: "doughnut",

    data: {

        labels: ["Critical", "High", "Medium"],

        datasets: [{

            data: [critical, high, medium]

        }]

    },

    options: {

        responsive: true

    }

});



const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");

function filterTable() {

    const search = searchInput.value.toLowerCase();
    const status = statusFilter.value;

    const rows = document.querySelectorAll("#alertTable tr");

    rows.forEach(row => {

        const text = row.innerText.toLowerCase();

        const badge = row.querySelector(".badge");

        const rowStatus = badge ? badge.innerText.trim() : "";

        const searchMatch = text.includes(search);
        const statusMatch = status === "" || rowStatus === status;

        row.style.display = searchMatch && statusMatch ? "" : "none";

    });

}

searchInput.addEventListener("keyup", filterTable);

statusFilter.addEventListener("change", filterTable);


// Manual Refresh Button
const refreshBtn = document.querySelector(".btn-primary");

if (refreshBtn) {

    refreshBtn.addEventListener("click", () => {

        location.reload();

    });

}

// Auto Refresh every 10 seconds
setInterval(() => {

    location.reload();

}, 10000);