document.addEventListener("DOMContentLoaded", function () {
  const studentsButton = document.getElementById("students-button");
  const studentOptions = document.getElementById("student-options");

  studentsButton.addEventListener("click", function () {
    studentOptions.style.display = studentOptions.style.display === "none" ? "block" : "none";
  });
});

function showStudents() {
  // Implement this function to show the default view when clicking Home
}

function studentsInfoButton() {
  fetch("/teacher/studentsInfo", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      const studentsInfoContainer = document.getElementById("info");
      studentsInfoContainer.innerHTML = `
        <div class="table-container">
          <h4 class="student-font">Students Info</h4>
          <table class="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>City</th>
                <th>Phone</th>
                <th>Gender</th>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
        </div>`;
      const tbody = studentsInfoContainer.querySelector("tbody");
      data.students.forEach((student) => {
        const rt = document.createElement("tr");
        rt.innerHTML = `
          <td class="student-font">${student.name}</td>
          <td class="student-font">${student.age}</td>
          <td class="student-font">${student.city}</td>
          <td class="student-font">${student.phone}</td>
          <td class="student-font">${student.gender}</td>
        `;
        tbody.appendChild(rt);
      });
    })
    .catch((error) => {
      console.error("Error fetching students info:", error);
    });
}

function studentsGradesButton() {
  fetch("/teacher/studentsGrades", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const studentsContainer = document.getElementById("info");
      studentsContainer.innerHTML = `
        <h2 class="students-title">Student Grades</h2>
        <p class="student-count">Total Students: ${data.count}</p>
        <div class="students-grid"></div>
      `;
      const studentsGrid = studentsContainer.querySelector(".students-grid");
      
      data.students.forEach((student) => {
        const card = document.createElement("div");
        card.className = "student-card";
        card.innerHTML = `
          <div class="student-avatar">
            <i class="fas fa-user-graduate"></i>
          </div>
          <h3 class="student-name">${student.name}</h3>
          <p class="student-grade">Grade: <span class="grade">${student.grade}</span></p>
          <div class="card-actions">
            <button class="update-button btn btn-primary" data-id="${student.id}">
              <i class="fa-regular fa-pen-to-square"></i> Update Grade
            </button>
            <a href="mailto:${student.email}" class="send-mail btn btn-secondary">
              <i class="fa-regular fa-envelope"></i> Send Email
            </a>
          </div>
        `;
        
        const updateButton = card.querySelector(".update-button");
        updateButton.addEventListener("click", function() {
          const gradeSpan = card.querySelector(".grade");
          const currentGrade = gradeSpan.textContent;
          
          const updateForm = document.createElement("div");
          updateForm.className = "update-form";
          updateForm.innerHTML = `
            <input type="number" class="update-grade" value="${currentGrade}">
            <button class="btn btn-success confirm-button">
              <i class="fa-solid fa-check"></i> Confirm
            </button>
          `;
          
          gradeSpan.parentNode.replaceChild(updateForm, gradeSpan);
          
          const confirmButton = updateForm.querySelector(".confirm-button");
          confirmButton.addEventListener("click", function() {
            const newGrade = updateForm.querySelector(".update-grade").value;
            
            if (newGrade === "") {
              updateForm.parentNode.replaceChild(gradeSpan, updateForm);
              return;
            }
            
            fetch("/editGrade", {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                id: student.id,
                grade: newGrade,
              }),
            })
              .then((response) => {
                if (!response.ok) {
                  throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
              })
              .then((data) => {
                gradeSpan.textContent = newGrade;
                updateForm.parentNode.replaceChild(gradeSpan, updateForm);
              })
              .catch((error) => console.error("Error:", error));
          });
        });
        
        studentsGrid.appendChild(card);
      });
    })
    .catch((error) => {
      console.error("Error fetching students:", error);
    });
}

function passedTheTestButton() {
  fetch("/teacher/passedStudents", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const studentsContainer = document.getElementById("info");
      studentsContainer.innerHTML = `
        <div class="table-container">
          <h4 class="student-font">Students Who Passed The Test</h4>
          <table class="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Grade</th>
              </tr>
            </thead>
            <tbody>
            </tbody>
          </table>
        </div>`;
      const tbody = studentsContainer.querySelector("tbody");
      data.students.forEach((student) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${student.name}</td>
          <td>${student.grade}</td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch((error) => {
      console.error("Error fetching passed students:", error);
    });
}

function profile() {
  fetch("/teacher/profile", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const profileContainer = document.getElementById("info");
      profileContainer.innerHTML = `
        <div class="profile-card">
          <h2>Teacher Profile</h2>
          <div class="profile-item">
            <h3>First Name:</h3>
            <p>${data.info.first_name}</p>
            <button class="btn btn-primary" onclick="editProfileField('first_name')">Edit</button>
          </div>
          <div class="profile-item">
            <h3>Last Name:</h3>
            <p>${data.info.last_name}</p>
            <button class="btn btn-primary" onclick="editProfileField('last_name')">Edit</button>
          </div>
          <div class="profile-item">
            <h3>Email:</h3>
            <p>${data.info.email}</p>
            <button class="btn btn-primary" onclick="editProfileField('email')">Edit</button>
          </div>
          <div class="profile-item">
            <h3>City:</h3>
            <p>${data.info.city}</p>
            <button class="btn btn-primary" onclick="editProfileField('city')">Edit</button>
          </div>
        </div>
      `;
    })
    .catch((error) => {
      console.error("Error fetching profile:", error);
    });
}

function editProfileField(field) {
  // Implement the edit functionality for each profile field
  // You can use a modal or inline editing
  console.log(`Editing ${field}`);
}

function logOut() {
  fetch("/logout", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Network response was not ok.");
      }
    })
    .then((data) => {
      window.location.href = data.redirect;
    })
    .catch((error) => console.error("Error:", error));
}