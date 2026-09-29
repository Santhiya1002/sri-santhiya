const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const levelContainer = document.getElementById("levelContainer");
const level = document.getElementById("level");

const submitButton = document.getElementById("submitButton");

const loading = document.getElementById("loading");
const resultSection = document.getElementById("resultSection");
const result = document.getElementById("result");

const errorSection = document.getElementById("errorSection");
const errorMessage = document.getElementById("errorMessage");

console.log("EduGenie JavaScript loaded");


task.addEventListener("change", function () {

    if (task.value === "learn") {
        levelContainer.classList.remove("hidden");
    } else {
        levelContainer.classList.add("hidden");
    }

});


submitButton.addEventListener("click", async function () {

    console.log("Generate button clicked");

    const text = inputText.value.trim();

    if (!text) {
        showError("Please enter a question, topic, or text.");
        return;
    }

    hideError();

    resultSection.classList.add("hidden");
    loading.classList.remove("hidden");

    submitButton.disabled = true;

    let endpoint;
    let body;


    if (task.value === "qa") {

        endpoint = "/qa";

        body = {
            text: text
        };

    } else if (task.value === "explain") {

        endpoint = "/explain";

        body = {
            text: text
        };

    } else if (task.value === "quiz") {

        endpoint = "/quiz";

        body = {
            text: text
        };

    } else if (task.value === "summarize") {

        endpoint = "/summarize";

        body = {
            text: text
        };

    } else if (task.value === "learn") {

        endpoint = "/learn/recommendations";

        body = {
            text: text,
            level: level.value
        };

    } else {

        showError("Please select a valid learning task.");

        loading.classList.add("hidden");
        submitButton.disabled = false;

        return;
    }


    console.log("Sending request:", endpoint);
    console.log("Request body:", body);


    try {

        const response = await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(body)

        });


        console.log("Server response:", response.status);


        const data = await response.json();

        console.log("Response data:", data);


        if (!response.ok) {

            throw new Error(
                data.detail || "Server returned an error."
            );

        }


        displayResult(data);


    } catch (error) {

        console.error("EduGenie error:", error);

        showError(
            error.message || "Something went wrong."
        );

    } finally {

        loading.classList.add("hidden");

        submitButton.disabled = false;

    }

});


function displayResult(data) {

    resultSection.classList.remove("hidden");


    if (data.result) {

        result.textContent = data.result;

        return;
    }


    if (data.questions) {

        result.innerHTML = "";


        data.questions.forEach(function (question, index) {

            const questionBox =
                document.createElement("div");

            questionBox.style.marginBottom = "25px";


            const title =
                document.createElement("h3");

            title.textContent =
                (index + 1) + ". " + question.question;

            questionBox.appendChild(title);


            question.options.forEach(function (option) {

                const optionElement =
                    document.createElement("p");

                optionElement.textContent =
                    "• " + option;

                questionBox.appendChild(optionElement);

            });


            const answer =
                document.createElement("p");

            answer.style.marginTop = "8px";

            answer.textContent =
                "Correct answer: " +
                question.correct_answer;

            questionBox.appendChild(answer);


            result.appendChild(questionBox);

        });

        return;
    }


    result.textContent =
        JSON.stringify(data, null, 2);

}


function showError(message) {

    errorMessage.textContent = message;

    errorSection.classList.remove("hidden");

}


function hideError() {

    errorSection.classList.add("hidden");

}