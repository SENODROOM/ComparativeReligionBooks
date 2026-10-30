const API_URL = "http://127.0.0.1:8000/ask";


const questionInput =
    document.getElementById("question");

const messages =
    document.getElementById("messages");

const welcome =
    document.getElementById("welcome");


/* =================================
   ASK QUESTION
================================= */

async function askQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    // Hide welcome screen
    welcome.style.display = "none";


    // Add user message
    addUserMessage(question);


    // Clear input
    questionInput.value = "";

    autoResize();


    // Show typing indicator
    const typingId =
        showTyping();


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        const data =
            await response.json();


        // Remove typing
        removeTyping(typingId);


        // Add AI answer
        addAIMessage(
            data.answer,
            data.sources
        );


    } catch (error) {

        removeTyping(typingId);


        addAIMessage(
            "I couldn't connect to the AI server. Please make sure the backend is running on http://127.0.0.1:8000.",
            []
        );


        console.error(error);
    }

}


/* =================================
   USER MESSAGE
================================= */

function addUserMessage(text) {

    const message =
        document.createElement("div");

    message.className =
        "message user";


    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent =
        text;


    message.appendChild(bubble);

    messages.appendChild(message);


    scrollToBottom();
}


/* =================================
   AI MESSAGE
================================= */

function addAIMessage(answer, sources) {

    const message =
        document.createElement("div");

    message.className =
        "message ai";


    const row =
        document.createElement("div");

    row.className =
        "ai-row";


    const avatar =
        document.createElement("div");

    avatar.className =
        "ai-avatar";

    avatar.textContent =
        "✦";


    const content =
        document.createElement("div");


    const label =
        document.createElement("div");

    label.className =
        "message-label";

    label.textContent =
        "AnonymousThinker";


    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent =
        answer;


    content.appendChild(label);

    content.appendChild(bubble);


    row.appendChild(avatar);

    row.appendChild(content);

    message.appendChild(row);


    messages.appendChild(message);


    /* Sources */

    if (
        sources &&
        sources.length > 0
    ) {

        const sourceList =
            document.createElement("div");

        sourceList.className =
            "source-list";


        sources.forEach(source => {

            const chip =
                document.createElement("div");

            chip.className =
                "source-chip";

            chip.textContent =
                "📖 " + source;

            sourceList.appendChild(chip);

        });


        messages.appendChild(sourceList);
    }


    scrollToBottom();
}


/* =================================
   TYPING INDICATOR
================================= */

function showTyping() {

    const id =
        "typing-" +
        Date.now();


    const message =
        document.createElement("div");

    message.className =
        "message ai";

    message.id =
        id;


    message.innerHTML = `
        <div class="ai-row">

            <div class="ai-avatar">
                ✦
            </div>

            <div>

                <div class="message-label">
                    AnonymousThinker
                </div>

                <div class="message-bubble">

                    <div class="typing">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>

                </div>

            </div>

        </div>
    `;


    messages.appendChild(message);


    scrollToBottom();


    return id;
}


function removeTyping(id) {

    const element =
        document.getElementById(id);


    if (element) {

        element.remove();

    }
}


/* =================================
   QUICK QUESTION
================================= */

function setQuestion(question) {

    questionInput.value =
        question;


    autoResize();


    questionInput.focus();
}


/* =================================
   ENTER TO SEND
================================= */

function handleEnter(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        askQuestion();
    }
}


/* =================================
   TEXTAREA AUTO RESIZE
================================= */

questionInput.addEventListener(
    "input",
    autoResize
);


function autoResize() {

    questionInput.style.height =
        "auto";


    questionInput.style.height =
        Math.min(
            questionInput.scrollHeight,
            130
        ) + "px";
}


/* =================================
   NEW CHAT
================================= */

function newChat() {

    messages.innerHTML = "";

    questionInput.value = "";

    autoResize();


    welcome.style.display =
        "block";


    questionInput.focus();
}


/* =================================
   SCROLL
================================= */

function scrollToBottom() {

    setTimeout(() => {

        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
        });

    }, 50);
}