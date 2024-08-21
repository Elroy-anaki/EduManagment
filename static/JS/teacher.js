function isPowerfulPassword(password) {
  if (password === "") {
    return { message: "The password cannot be empty!", isValid: false };
  }
  if (password.length < 8) {
    return {
      message: "The password must be at least 8 characters long!",
      isValid: false,
    };
  }

  let digitCount = 0;
  let upperCount = 0;

  for (let char of password) {
    if (/\d/.test(char)) {
      digitCount++;
    } else if (/[A-Z]/.test(char)) {
      upperCount++;
    }
  }

  if (digitCount < 3) {
    return {
      message: "The password must contain at least 3 digits!",
      isValid: false,
    };
  }
  if (upperCount < 2) {
    return {
      message: "The password must contain at least 2 uppercase letters!",
      isValid: false,
    };
  }
  return { message: "The password is powerful!", isValid: true };
}
document.addEventListener("DOMContentLoaded", function () {
  const studentsButton = document.getElementById("students-button");
  const studentOptions = document.getElementById("student-options");

  studentsButton.addEventListener("click", function () {
    studentOptions.style.display =
      studentOptions.style.display === "none" ? "block" : "none";
  });
});

function homeButton() {
  fetch("/home", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(response.message)
  } return response.json()
}).then((data) => {
  window.location.href = data.redirect
}).catch((error) => {alert(error)})


};

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
        updateButton.addEventListener("click", function () {
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
          confirmButton.addEventListener("click", function () {
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
              .then(() => {
                gradeSpan.textContent = newGrade;
                updateForm.parentNode.replaceChild(gradeSpan, updateForm);
                return studentsGradesButton();
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
        <div class="profile-container">
          <div class="profile-card">
            <div class="profile-header">
              <h2>${data.info.first_name + " " + data.info.last_name}</h2>
              <div class="profile-avatar">
                <i class="fa-solid fa-chalkboard-user"></i>
              </div>
            </div>
            <div class="profile-content">
              <div class="profile-item">
                <label>First Name:</label>
                <input id="firstName" value=${data.info.first_name}></input>
              </div>
              <div class="profile-item">
                <label>Last Name:</label>
                <input id="lastName" value=${data.info.last_name}></input>
              </div>
              <div class="profile-item">
                <label>Email:</label>
                <input id="email" value=${data.info.email}></input>
              </div>
              <div class="profile-item">
                <label>Password:</label>
                <input id="password" value=${data.info.password}></input>
              </div>
              <div class="profile-item">
                <label>Phone:</label>
                <input id="phone" value=${data.info.phone}></input>
              </div>
              <div class="profile-item">
                <label>City:</label>
                <input id="city" value=${data.info.city}></input>
              </div>
            </div>
              <button type="button" class="edit-personal-details" onclick=saveChanges()><p>Save Changes</p></button>
              
          </div>
          
        </div>
      `;
    })
    .catch((error) => {
      console.error("Error fetching profile:", error);
    });
}

function saveChanges() {
  const firstName = document.getElementById("firstName").value;
  const lastName = document.getElementById("lastName").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const phone = document.getElementById("phone").value;
  const city = document.getElementById("city").value;
  const checkPassword = isPowerfulPassword(password);
  if (firstName === "" || lastName === "") {
    alert("first and last name requrid!")
    return;
  }
  if (!checkPassword.isValid) {
    alert(checkPassword.message);
    return profile();
  }
  fetch("/teacher/profile/editPersonalInfo", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      firstName: firstName,
      lastName: lastName,
      email: email,
      password: password,
      phone: phone,
      city: city,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then((data) => {
      console.log(data.me)
      window.location.href = data.redirect;
    })
    .catch((error) => alert(error));
}

function assignmentsButton() {
  fetch("/teacher/assignments", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      const assignmentsContainer = document.getElementById("info");
      assignmentsContainer.innerHTML = `
      
      <div class="task-container">
        <h2>Count of Assignments: ${data.assignments.length}</h2>
        <div class="task-header">Your Assignment</div>
        <div class="task-list"></div>
        <div class="edit-container">
          <div id="editTitle"></div>
          <div id="editDescription"></div>
          <div id="confirmAssignment"></div>
        </div>
        <div class="add-task" onclick="addAssignment()">+ Add a new Assignment</div>
        <div id="new-assignment"></div>
      </div>`;

      const taskList = assignmentsContainer.querySelector(".task-list");
      data.assignments.forEach((assignment) => {
        const taskWrapper = document.createElement("div");
        taskWrapper.classList.add("task-wrapper");

        const taskID = document.createElement("div");
        taskID.id = "TaskID";
        taskID.textContent = assignment.id;
        taskID.style.display = "none"; // הסתרת ה-ID כפי שביקשת

        const taskTitle = document.createElement("div");
        taskTitle.classList.add("task-title");
        taskTitle.textContent = assignment.title;

        const taskDescription = document.createElement("div");
        taskDescription.classList.add("task-description");
        taskDescription.textContent = assignment.description;
        taskDescription.style.display = "none";

        const showButton = document.createElement("button");
        showButton.textContent = "Show";
        showButton.className = "show-hide-task-button";

        showButton.addEventListener("click", () => {
          if (taskTitle.textContent === assignment.title) {
            taskTitle.textContent = assignment.description;
            showButton.textContent = "Hide";
          } else {
            taskTitle.textContent = assignment.title;
            showButton.textContent = "Show";
          }
        });

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.className = "edit-task-button";
        editButton.addEventListener("click", () => {
          document.getElementById(
            "editTitle"
          ).innerHTML = `<input id="newTitle" value="${assignment.title}"></input>`;
          document.getElementById(
            "editDescription"
          ).innerHTML = `<input id="newDescription" value="${assignment.description}"></input>`;
          document.getElementById(
            "confirmAssignment"
          ).innerHTML = `<button onclick="confirmAssignment(${assignment.id})">Confirm</button>`;
        });
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-task-button";
        deleteButton.addEventListener("click", () => {
          fetch("/teacher/Assignment/deleteAssignmnet", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              id: assignment.id,
            }),
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error(response.message);
              }
              return response.json();
            })
            .then((data) => {
              alert(data.message);
              return assignmentsButton();
            })
            .catch((error) => alert(error));
        });

        taskWrapper.appendChild(taskID);
        taskWrapper.appendChild(taskTitle);
        taskWrapper.appendChild(showButton);
        taskWrapper.appendChild(editButton);
        taskWrapper.appendChild(deleteButton);
        taskWrapper.appendChild(taskDescription);
        taskList.appendChild(taskWrapper);
      });
    })
    .catch((error) => alert(error.message));
}

function addAssignment() {
  const newAssignment = document.getElementById("new-assignment");
  newAssignment.innerHTML = `
  <input id="newAssignmentTitle" placeholder="Title..."></input>
  <input id="newAssignmentDescription" placeholder="Description..."></input>
  `;
  const addNewAssignmentButton = document.createElement("button");
  addNewAssignmentButton.textContent = "Add Assignment";
  addNewAssignmentButton.addEventListener("click", () => {
    const title = document.getElementById("newAssignmentTitle").value;
    const description = document.getElementById(
      "newAssignmentDescription"
    ).value;
    if (title === "" || description === "") {
      alert("Title and Description are required");
      return;
    }
    fetch("/teacher/Assignment/addAssignmnet", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
        description: description,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(response.message);
        }
        return response.json();
      })
      .then((data) => {

        return assignmentsButton();
      })
      .catch((error) => alert(error));
  });
  newAssignment.appendChild(addNewAssignmentButton);
}

function confirmAssignment(id) {
  const title = document.getElementById("newTitle").value;
  const description = document.getElementById("newDescription").value;
  fetch("/teacher/Assignment/editAssignmnet", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      title: title,
      description: description,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then((data) => {
      
      return assignmentsButton();
    })
    .catch((error) => {
      alert(error);
    });
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
