function submitForm() {
    var newName = document.getElementById("new_name").value;
    var newDOB = document.getElementById("new_dob").value;

    if (!newName) {
        alert('Please enter a valid new name.');
        return;
    }

    if (!newDOB) {
        alert('Please select a valid date of birth.');
        return;
    }

    var formData = {
        "username": username,  
        "new_name": newName,
        "new_dob": newDOB
    };

    fetch("/updateprofile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Parsed Response:', data);
        if (data.success) {
            console.log('Success:', data);    
            document.getElementById("name").innerText = `Name: ${newName}`;
            document.getElementById("dateOfBirth").innerText = `Date of Birth: ${newDOB}`;
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
