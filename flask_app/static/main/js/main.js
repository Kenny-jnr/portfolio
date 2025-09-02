// Get feedback elements
const feedbackButton = document.getElementById("feedback"); // gets feedback id
const form_container = document.getElementById("feedback-form-container"); //get the container of the form
let failed_attempts = 0;

if (localStorage.getItem("formVisible") === "true") {
  // storing the present form visisbility, this will remain accross each page
  form_container.style.display = "block";
} else {
  form_container.style.display = "none";
}

feedbackButton.addEventListener("click", function () {
  // just toggles to show the form whenever the feedback button is clicked on
  if (form_container.style.display === "none") {
    form_container.style.display = "block"; // Show the form
    localStorage.setItem("formVisible", "true");
  } else {
    form_container.style.display = "none"; // Hide the form
    localStorage.setItem("formVisible", "false");
  }
});

const send = document.querySelector(".send"); // action that occurs when the send button is hit.

send.addEventListener("click", function () {
  form_container.style.display = "none"; // Hides the form
  localStorage.setItem("formVisible", "false");
});

//  used to adjust the content justification when the item within the container is too small for a scroll bar
window.addEventListener("load", () => {
  const pContainer = document.querySelector(".p-container");

  // Check if the container's content is overflowing
  const isOverflowing = pContainer.scrollHeight > pContainer.clientHeight;

  if (!isOverflowing) {
    pContainer.classList.add("no-scrollbar");
  } else {
    pContainer.classList.remove("no-scrollbar");
  }
});

// for the login credentials

document
  .getElementById("login-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent normal form submission

    const user_email = document.getElementById("user-email").value;
    const user_password = document.getElementById("user-password").value;

    try {
      const response = await fetch("/processlogin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_email, user_password }),
      });

      const data = await response.json();
      print(data);

      const message = document.getElementById("failed-attempts-text");

      // renders how many failed sign in attempts
      if (data.status === 2) {
        failed_attempts += 1;

        message.textContent = `Authentication Failure: ${failed_attempts}`;
        message.style.display = "block";
        message.style.color = "red";
      } else {
        failed_attempts = 0; // restart counter
        message.style.display = "none";
        window.location.href = data.redirect_url;
      }
    } catch (error) {
      console.error("Login error:", error);
      document.getElementById("message").textContent =
        "An error occurred while logging in.";
    }
  });
