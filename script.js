document.getElementById("sendBtn").addEventListener("click", function () {
  const feedback = document.getElementById("feedbackText").value.trim();

  if (!feedback) {
    alert("Please write some feedback before submitting.");
    return;
  }

  fetch("https://discord.com/api/webhooks/1362275778682818690/iE04DIwklUddKS9IpiFhUnBObT1uuW0tw4uebATvY-uKAS0gbqj2ruoFywuDcG9fmNyr", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      content: `**New Feedback:**\n${feedback}`
    })
  })
    .then(response => {
      if (response.ok) {
        alert("Feedback sent successfully!");
        document.getElementById("feedbackText").value = "";
      } else {
        alert("Failed to send feedback.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Error sending feedback.");
    });
});
