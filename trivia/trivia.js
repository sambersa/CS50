document.querySelectorAll(".trivia button").forEach(button => {
    button.addEventListener("click", function() {
        const message = document.getElementById('message');
        if (this.textContent !== '7' && this.textContent !== 'A kid') {
            message.textContent = 'Incorrect!';
            message.style.color = 'red'; // Changing color to red if incorrect
        } else {
            message.textContent = 'Correct!';
            message.style.color = 'green'; // Changing color to green if correct
        }
    });
});

document.getElementById('checkDavid').addEventListener('click', function()
 {
    const userAnswer = document.getElementById('david').value.trim().toLowerCase();
    const correctAnswer = 'David Malan'.toLowerCase();
    const message = document.getElementById('davidMessage');

    if (userAnswer === correctAnswer) {
        message.textContent = 'Correct!';
        message.className = 'correct';
        message.style.color = 'green'; // Changing color to green if correct
    }

    else {
        message.textContent = 'Incorrect!'
        message.className = 'incorrect';
        message.style.color = 'red'; // Changing color to red if incorrect
    }
    message.style.display = 'block';
});


