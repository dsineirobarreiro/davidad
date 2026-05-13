let chart = null;
let compatibilityChart = null;
let ethicalChart = null;

async function loadQuestionStats(day) {

    const response = await fetch(
        `/api/question-stats/${day}/`
    );

    const result = await response.json();

    const labels = result.data.map(x => x.label);
    const counts = result.data.map(x => x.count);

    const ctx = document
        .getElementById('questionChart');

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {

        type: 'pie',

        data: {

            labels: labels,

            datasets: [{
                data: counts
            }]
        },

        options: {
            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            }
        }
    });
}

async function loadUserQuestion(userId, questionId) {

    const res = await fetch(
        `/api/user-question/${userId}/${questionId}/`
    );

    const data = await res.json();

    const container =
        document.getElementById("uqResult");

    if (!data.answer) {

        container.innerHTML = `
            <div class="alert alert-warning">
                No ha respondido esta pregunta
            </div>
        `;

        return;
    }

    let html = "";

    if (Array.isArray(data.answer)) {

        html = `
            <div class="card p-3">
                <div class="fw-bold mb-2">
                    ${data.question}
                </div>
                <ol>
                    ${data.answer.map(a => `<li>${a}</li>`).join("")}
                </ol>
            </div>
        `;

    } else {

        html = `
            <div class="card p-3">
                <div class="fw-bold mb-2">
                    ${data.question}
                </div>
                <div>
                    ${data.answer}
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

async function loadCompatibilityTimeline() {

    const user1 =
        document.getElementById(
            "matchGraph1Select"
        ).value;

    const user2 =
        document.getElementById(
            "matchGraph2Select"
        ).value;

    const response = await fetch(
        `/api/compatibility-timeline/${user1}/${user2}/`
    );

    const data = await response.json();

    const ctx = document
        .getElementById('matchGraphContainer');

    if (compatibilityChart) {
        compatibilityChart.destroy();
    }

    compatibilityChart = new Chart(ctx, {

        type: 'line',

        data: {

            labels: data.labels,

            datasets: [{

                label:
                    `${data.user1} vs ${data.user2}`,

                data: data.scores,

                tension: 0.3,

                fill: true,

                borderColor: '#d84141',
                backgroundColor: '#eb363677',


            }]
        },

        options: {

            responsive: true,
            maintainAspectRatio: false,

            scales: {

                y: {
                    beginAtZero: true,
                    max: 100,

                    ticks: {
                        callback: value => value + "%"
                    }
                }

            },

            interaction: {
                mode: 'index',
                intersect: false
            },

            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            }

        }

    });
}

async function loadUserMatches(userId, range) {

    const response = await fetch(
        `/api/user-matches/${userId}/`
    );

    const result = await response.json();

    const container = document.getElementById(
        "matchesContainer"
    );

    container.innerHTML = "";

    result.matches.forEach(match => {

        var percentage = range == "global" ? match.score : match.percentage;

        container.innerHTML += `

            <div class="mb-3">

                <div class="d-flex justify-content-between mb-1">

                    <strong>
                        ${match.username}
                    </strong>

                    <span>
                        ${percentage}%
                    </span>

                </div>

                <div class="progress">

                    <div
                        class="progress-bar"
                        role="progressbar"
                        style="width: ${percentage}%">

                    </div>

                </div>

            </div>

        `;
    });
}

async function loadEthicalProfile(userId) {

    const response = await fetch(
        `/api/user-ethical-profile/${userId}/`
    );

    const data = await response.json();

    const labels =
        data.profiles.map(p => p.profile);

    const scores =
        data.profiles.map(p => p.score);

    const ctx =
        document.getElementById("ethicalChart");

    if (ethicalChart) {
        ethicalChart.destroy();
    }

    ethicalChart = new Chart(ctx, {

        type: 'polarArea',

        data: {

            labels: labels,

            datasets: [{

                data: scores,

                backgroundColor: [

                    '#ff6385c7',
                    '#36a2ebc7',
                    '#ffce56c7',
                    '#4bc0c0c7',
                    '#9966ffc7',
                    '#ff9f40c7'

                ]

            }]
        },

        options: {

            responsive: true,
            maintainAspectRatio: false,

            scales: {

                r: {

                    min: 0,
                    max: 100,

                    ticks: {

                        color: 'white',

                        backdropColor: 'transparent'

                    },

                    grid: {
                        color: 'rgba(255,255,255,0.15)'
                    },

                    angleLines: {
                        color: 'rgba(255,255,255,0.15)'
                    },

                    pointLabels: {

                        color: 'white',

                        font: {
                            size: 14
                        }

                    }

                }

            },

            plugins: {

                legend: {

                    labels: {
                        color: 'white'
                    }

                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            return `${context.label}: ${context.raw}%`;

                        }

                    }

                }

            }

        }

    });

}

document.addEventListener("DOMContentLoaded", () => {

    const questionSelect =
        document.getElementById("questionSelect");

    const userSelect =
        document.getElementById("userSelect");
    
    const rangeSelect =
        document.getElementById("rangeSelect");

    const uqUser =
        document.getElementById("uqUser");

    const uqQuestion =
        document.getElementById("uqQuestion");

    const matchGraph1Select =
        document.getElementById("matchGraph1Select");
    
    const matchGraph2Select =
        document.getElementById("matchGraph2Select");

    const ethicalUserSelect =
        document.getElementById("ethicalUserSelect");

    loadQuestionStats(questionSelect.value);
    loadUserMatches(userSelect.value, rangeSelect.value);
    loadEthicalProfile(ethicalUserSelect.value);

    questionSelect.addEventListener("change", () => {

        loadQuestionStats(questionSelect.value);

    });

    matchGraph1Select.addEventListener("change", loadCompatibilityTimeline);
    matchGraph2Select.addEventListener("change", loadCompatibilityTimeline);

    userSelect.addEventListener("change", () => {

        loadUserMatches(userSelect.value, rangeSelect.value);

    });

    rangeSelect.addEventListener("change", () => {

        loadUserMatches(userSelect.value, rangeSelect.value);

    });

    function refresh() {
        loadUserQuestion(
            uqUser.value,
            uqQuestion.value
        );
    }

    uqUser.addEventListener("change", refresh);
    uqQuestion.addEventListener("change", refresh);

    refresh();

    ethicalUserSelect.addEventListener("change", () => {

        loadEthicalProfile(ethicalUserSelect.value);

    }
);

});