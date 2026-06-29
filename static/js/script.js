/*
==========================================================
CandidateOne

Frontend JavaScript


==========================================================
*/

"use strict";

/* =======================================================
   DOM Ready
======================================================= */

document.addEventListener("DOMContentLoaded", () => {

    console.log("CandidateOne UI Loaded.");

    initializeTooltips();

    initializeFileInputs();

    initializeUploadForm();

    initializeJsonViewer();

    initializeCards();

});

/* =======================================================
   Bootstrap Tooltips
======================================================= */

function initializeTooltips() {

    const tooltipTriggerList = [].slice.call(

        document.querySelectorAll(

            '[data-bs-toggle="tooltip"]'

        )

    );

    tooltipTriggerList.map(

        tooltip => new bootstrap.Tooltip(tooltip)

    );

}

/* =======================================================
   File Upload Labels
======================================================= */

function initializeFileInputs() {

    const fileInputs = document.querySelectorAll(

        'input[type="file"]'

    );

    fileInputs.forEach(input => {

        input.addEventListener(

            "change",

            function () {

                if (this.files.length > 0) {

                    console.log(

                        this.files[0].name

                    );

                }

            }

        );

    });

}

/* =======================================================
   Upload Form
======================================================= */

function initializeUploadForm() {

    const form = document.getElementById(

        "uploadForm"

    );

    if (!form) return;

    form.addEventListener(

        "submit",

        function () {

            const button = document.getElementById(

                "submitBtn"

            );

            if (button) {

                button.disabled = true;

                button.innerHTML =

                    '<span class="spinner-border spinner-border-sm"></span> Processing...';

            }

            const loading = document.getElementById(

                "loading"

            );

            if (loading) {

                loading.style.display = "block";

            }

        }

    );

}

/* =======================================================
   JSON Viewer
======================================================= */

function initializeJsonViewer() {

    const viewers = document.querySelectorAll(

        ".json-view"

    );

    viewers.forEach(view => {

        view.addEventListener(

            "dblclick",

            function () {

                navigator.clipboard.writeText(

                    this.innerText

                );

                showToast(

                    "JSON copied to clipboard."

                );

            }

        );

    });

}

/* =======================================================
   Card Hover Effect
======================================================= */

function initializeCards() {

    const cards = document.querySelectorAll(

        ".card"

    );

    cards.forEach(card => {

        card.addEventListener(

            "mouseenter",

            function () {

                this.style.transform =

                    "translateY(-6px)";

            }

        );

        card.addEventListener(

            "mouseleave",

            function () {

                this.style.transform =

                    "translateY(0px)";

            }

        );

    });

}

/* =======================================================
   Toast Notification
======================================================= */

function showToast(message) {

    const toast = document.createElement("div");

    toast.className =

        "position-fixed bottom-0 end-0 p-3";

    toast.style.zIndex = "99999";

    toast.innerHTML = `

<div class="toast show">

<div class="toast-header bg-primary text-white">

<strong class="me-auto">

CandidateOne

</strong>

<button

type="button"

class="btn-close"

onclick="this.parentElement.parentElement.parentElement.remove();">

</button>

</div>

<div class="toast-body">

${message}

</div>

</div>

`;

    document.body.appendChild(

        toast

    );

    setTimeout(() => {

        toast.remove();

    }, 2500);

}

/* =======================================================
   Scroll to Top
======================================================= */

window.addEventListener(

    "scroll",

    function () {

        const button = document.getElementById(

            "scrollTop"

        );

        if (!button) return;

        if (window.scrollY > 250) {

            button.style.display = "block";

        }

        else {

            button.style.display = "none";

        }

    }

);

/* =======================================================
   Scroll Function
======================================================= */

function scrollToTop() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}

/* =======================================================
   Copy JSON Button
======================================================= */

function copyJson(id) {

    const element = document.getElementById(id);

    if (!element) return;

    navigator.clipboard.writeText(

        element.innerText

    );

    showToast(

        "Copied successfully."

    );

}

/* =======================================================
   Download Animation
======================================================= */

document.querySelectorAll(

    ".btn"

).forEach(button => {

    button.addEventListener(

        "click",

        function () {

            this.classList.add(

                "shadow-lg"

            );

        }

    );

});

/* =======================================================
   CandidateOne Ready
======================================================= */

console.log(

    "CandidateOne Ready."

);