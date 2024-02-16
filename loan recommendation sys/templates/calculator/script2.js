document.getElementById('loan-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get user input
    const loanAmount = parseFloat(document.getElementById('loan-amount').value);
    const interestRate = parseFloat(document.getElementById('interest-rate').value) / 100 / 12;
    const loanTenure = parseFloat(document.getElementById('loan-tenure').value);

    // Calculate monthly payment
    const monthlyPayment = calculateEMI(loanAmount, interestRate, loanTenure);

    // Display result
    const resultElement = document.getElementById('result');
    resultElement.innerHTML = `
        <h3>Monthly EMI: ₹${monthlyPayment.toFixed(2)}</h3>
    `;

    // Calculate and display EMI schedule
    const emiSchedule = calculateEMISchedule(loanAmount, interestRate, loanTenure);
    resultElement.innerHTML += '<h3>EMI Schedule:</h3>';
    emiSchedule.forEach((emi, index) => {
        resultElement.innerHTML += `<p>Month ${index + 1}: ₹${emi.toFixed(2)}</p>`;
    });
});

function calculateEMI(loanAmount, interestRate, loanTenure) {
    const numerator = loanAmount * interestRate * Math.pow(1 + interestRate, loanTenure);
    const denominator = Math.pow(1 + interestRate, loanTenure) - 1;
    return numerator / denominator;
}

function calculateEMISchedule(loanAmount, interestRate, loanTenure) {
    const monthlyPayment = calculateEMI(loanAmount, interestRate, loanTenure);
    const emiSchedule = [];
    for (let i = 0; i < loanTenure; i++) {
        emiSchedule.push(monthlyPayment);
    }
    return emiSchedule;
}
