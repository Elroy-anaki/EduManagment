document.addEventListener("DOMContentLoaded", function () {
  const studentsButton = document.getElementById("students-button");
  const studentOptions = document.getElementById("student-options");

  studentsButton.addEventListener("click", function () {
    if (studentOptions.style.display === "none") {
      studentOptions.style.display = "block";
    } else {
      studentOptions.style.display = "none";
    }
  });
});

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
      console.error("Error fetching passed students:", error);
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
        <div class="table-container">
        <h4 class="student-font">Count of Students: ${data.count} </h4>
          <table class="students-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Grade</th>
                <th>Update</th>
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
          <td class="student-font">${student.name}</td>
          <td>${student.grade}</td>
          <td><button class="update-button btn btn-success" data-id="${student.id}"><i class="fa-regular fa-pen-to-square"></i></button></td>
        `;
        const button = tr.querySelector(".update-button");
        button.addEventListener("click", function () {
          const inputElement = document.createElement("input");
          inputElement.type = "number";
          inputElement.className = "update-grade";
          inputElement.placeholder = "Enter new grade";

          const confirmButton = document.createElement("button");
          confirmButton.className = "btn btn-primary";
          confirmButton.innerHTML = `<i class="fa-solid fa-check"></i>`;

          const cell = this.parentNode;
          cell.innerHTML = "";
          cell.appendChild(inputElement);
          cell.appendChild(confirmButton);

          confirmButton.addEventListener("click", function () {
            const newGrade = inputElement.value;

            if (newGrade === "") {
              return studentsGradesButton();
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
                const gradeCell = tr.querySelector("td:nth-child(2)");
                gradeCell.textContent = newGrade;
                return studentsGradesButton();
              })
              .catch((error) => console.error("Error:", error));
          });
        });
        tbody.appendChild(tr);
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

function profileButton() {
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
      profileContainer.innerHTML = "";

      const profileFields = [
        { key: "first_name", label: "First Name", value: data.info.first_name },
        { key: "last_name", label: "Last Name", value: data.info.last_name },
        { key: "email", label: "Email", value: data.info.email },
        { key: "password", label: "Password", value: data.info.password },
        { key: "city", label: "City", value: data.info.city },
      ];

      // שימוש ב- forEach ליצירת אלמנטים עבור כל שדה
      profileFields.forEach((field) => {
        const fieldDiv = document.createElement("div");
        fieldDiv.className = "profile-item";
        fieldDiv.innerHTML = `
          <p id="${field.label}">${field.label}: ${field.value}</p>
          <button type="button" class="btn btn-primary">Edit</button>
        `;
        const button = fieldDiv.querySelector(".btn");
        button.addEventListener("click", function () {
          fetch("/editValue", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              key: field.key,
            }),
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.json();
            })
            .then((data) => {
              alert(data.message);
            })
            .catch((error) => console.error("Error:", error));
        });
        profileContainer.appendChild(fieldDiv);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
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