let currentMatchId = null;

let currentGiftButton = null;
let currentGiftSlot = null;
let currentTargetUser = null;

const guesses = {};

const modal = new bootstrap.Modal(
    document.getElementById("guessModal")
);

document.querySelectorAll(".guess-btn")
.forEach(button => {

    button.addEventListener("click", () => {

        currentMatchId =
            button.dataset.matchId;

        refreshDisabledUsers(currentMatchId);

        modal.show();

    });

});

document
.querySelectorAll(".user-choice-btn")
.forEach(button => {

    button.addEventListener("click", () => {

        const userId =
            button.dataset.userId;

        const username =
            button.dataset.username;

        // =====================
        // evitar repetidos
        // =====================

        const alreadyUsed =
            Object.entries(guesses)
            .some(([matchId, guessedId]) => {

                return guessedId == userId
                    && matchId != currentMatchId;

            });

        if (alreadyUsed) {
            return;
        }

        // =====================
        // guardar guess
        // =====================

        const currentGuess =
            guesses[currentMatchId];

        // =====================
        // toggle selección
        // =====================

        if (currentGuess == userId) {

            delete guesses[currentMatchId];

            sendUserMatchGuess(currentMatchId, null);

            console.log("Guess removed for match", currentMatchId);

            const guessButton =
                document.querySelector(
                    `.guess-btn[data-match-id="${currentMatchId}"]`
                );

            guessButton.innerText = "???";

            const guessMatch =
                document.querySelector(
                    `.match-card[data-match-id="${currentMatchId}"]`
                );

            guessMatch.classList.remove(
                "border-success",
                "border-danger"
            );

            guessMatch.classList.add(
                "border-secondary"
            );

            const row = document.querySelector(
                `.match-card[data-match-id="${currentMatchId}"]`
            );

            row
            .querySelectorAll(".gift-btn")
            .forEach(btn => {

                btn.disabled = true;

                btn.innerText = "???";

                btn.dataset.giftId = "";

                btn.classList.remove(
                    "border-success",
                    "border-danger"
                );

                btn.classList.add(
                    "border-secondary"
                );

                const checkBtn =
                row.querySelector(
                    ".check-gifts-btn"
                );

                checkBtn.disabled = true;

            });

            refreshDisabledUsers(currentMatchId);

            modal.hide();

            return;
        }

        guesses[currentMatchId] =
            userId;

        sendUserMatchGuess(currentMatchId, userId);

        // =====================
        // actualizar botón card
        // =====================

        const guessButton =
            document.querySelector(
                `.guess-btn[data-match-id="${currentMatchId}"]`
            );

        guessButton.innerText =
            username;

        // =====================
        // refrescar disabled
        // =====================

        refreshDisabledUsers(currentMatchId);

        modal.hide();

    });

});

async function sendUserMatchGuess(matchId, currentGuess) {

    await fetch(
        "/api/save-match-guess/",
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json",

                "X-CSRFToken":
                    getCSRFToken()

            },

            body: JSON.stringify({

                match_id: matchId,

                guessed_user_id: currentGuess

            })

        }
    );
}

function refreshDisabledUsers(matchId) {

    const usedUsers =
        Object.values(guesses);

    document
        .querySelectorAll(".user-choice-btn")
        .forEach(button => {

            const userId =
                button.dataset.userId;

            const isUsed =
                Object.values(guesses)
                .includes(userId);

            const currentGuess =
                guesses[matchId];

            const isCurrent =
                currentGuess == userId;

            // reset visual

            button.disabled = false;

            button.classList.remove(
                "opacity-50",
                "btn-outline-warning",
                "btn-outline-light"
            );

            // =====================
            // seleccionado actual
            // =====================

            if (isCurrent) {

                button.classList.add(
                    "btn-outline-warning"
                );

            }

            // =====================
            // usado por otro
            // =====================

            else if (isUsed) {

                button.disabled = true;

                button.classList.add(
                    "btn-outline-light",
                    "opacity-50"
                );

            }

            // =====================
            // libre
            // =====================

            else {

                button.classList.add(
                    "btn-outline-light"
                );

            }

        });

}

document
.getElementById("checkMatchesBtn")
.addEventListener("click", async () => {

    const payload = {

        guesses: Object.entries(guesses)
        .map(([match_id, guessed_user_id]) => ({

            match_id,
            guessed_user_id

        }))

    };

    console.log("Payload:", payload);

    const response = await fetch(
        "/api/check-match-guesses/",
        {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "X-CSRFToken": getCSRFToken()

            },

            body: JSON.stringify(payload)

        }
    );

    const data = await response.json();

    data.results.forEach(result => {

        const card = document.querySelector(
            `.match-card[data-match-id="${result.match_id}"]`
        );

        card.classList.remove(
            "border-danger",
            "border-success",
            "border-secondary"
        );

        card.classList.add(
            result.correct
                ? "border-success"
                : "border-danger"
        );

        const guessBtn =
            card.querySelector(".guess-btn");

        guessBtn.disabled = result.finished;

        if (!result.correct && result.finished) {

            guessBtn.innerText =
                result.real_username;

            delete guesses[result.match_id];

        }

        const giftsContainer =
            card.querySelector(
                ".revealed-gifts"
            );

        giftsContainer.innerHTML = `

            <div class="row g-2">

                ${result.gift_slots.map(g => `

                    <div class="col-4">

                        <div
                            class="card bg-secondary text-white p-3 text-center"
                            style="
                                transition: all 0.25s ease;
                            ">

                                ${g.name}

                        </div>

                    </div>

                `).join("")}

            </div>

        `;
    });

});

function getCSRFToken() {

    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

}

document.addEventListener("DOMContentLoaded", () => {

    document
    .querySelectorAll(".guess-btn")
    .forEach(button => {

        const matchId =
            button.dataset.matchId;

        const guessedUserId =
            button.dataset.guessedUserId;

        if (guessedUserId) {

            guesses[matchId] =
                guessedUserId;

        }

    });
});