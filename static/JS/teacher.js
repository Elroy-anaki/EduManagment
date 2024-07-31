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

function allStudentsButton() {
  fetch("/teacher/students", {
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
                  <th>Action</th>
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
            <td><button class="update-button btn btn-success" data-id="${student.id}">Update Grade</button></td>
          `;
        const button = tr.querySelector(".update-button");
        button.addEventListener("click", function () {
          alert(`You clicked ${student.id}!`);
        });
        tbody.appendChild(tr);
      });
    })
    .catch((error) => {
      console.error("Error fetching students:", error);
    });
}

function passedStudentsButton() {
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

function profileButton(){
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
        <div>
      <h3 id="current-name">name: ${data.name}</h3>
      <button type="button" class="btn btn-primary" onclick="openEditForm()">Edit</button>
    </div>
    <div id="update-name" style="display: none;">
      <input type="text" id="firstName" placeholder="first name">
      <input type="text" id="lastName" placeholder="last name">
      <button onclick="updateName()">Update</button>
    </div>
    <div> ${data.email}</div>
    <div> ${data.pass}</div>
    <div> ${data.city}</div>`


})}

















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

