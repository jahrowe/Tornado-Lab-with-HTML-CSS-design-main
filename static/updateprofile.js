function submitForm() {
    let new_name = document.getElementById("new_name").value;
    let new_dob = document.getElementById("new_dob").value;
    console.log("New Info:", new_name, new_dob);


    if (!new_name) {
        alert('Please enter a valid new name.');
        return;
    }


    let dateRegex = /^(Jan\.|Feb\.|Mar\.|Apr\.|May|Jun\.|Jul\.|Aug\.|Sep\.|Oct\.|Nov\.|Dec\.)(?:\s|\.|\s\.)\s?\d{1,2}$/;
    if (!dateRegex.test(new_dob)) {
        alert('Please enter a valid date of birth.');
        return;
    }


    fetch('/update_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ new_name, new_dob }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Parsed Response:', data);
        if (data.success) {
            console.log('Success:', data);    
            document.getElementById("name").innerText = `Name: ${new_name}`;
            document.getElementById("dateOfBirth").innerText = `Date of Birth: ${new_dob}`;
        } else {
            if (data.error === 'Invalid input') {
                alert('Invalid input. Please check your data and try again.');
            } else {
                alert(data.error || 'Error updating profile. Please try again.');              
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error updating profile. Please try again.');
    });
}
