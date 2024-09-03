function no() {
  alert("YOU NEED TO TEACH YOUR STUDENT ALL THE COURSES!!!!");
}

function deleteUser(userID) {
  fetch("/manager/deleteUser", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      userID: userID,
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
      window.location.reload();
    })
    .catch((error) => {
      alert(error);
    });
}

function showTeacherDetails() {
  var details = document.getElementById("new-teacher-details");
  if (details.style.display === "none" || details.style.display === "") {
    details.style.display = "block";
  } else {
    details.style.display = "none";
  }
}

function saveTeacher() {
  var firstName = document.getElementById("first_name").value;
  var lastName = document.getElementById("last_name").value;
  var email = document.getElementById("email").value;
  var courseID = document.getElementById("course").value;
  fetch("/manager/AddTeacher", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      firstName: firstName,
      lastName: lastName,
      email: email,
      courseID: courseID,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then((data) => {
      window.location = data.redirect;
    })
    .catch((error) => {
      alert(error);
    });
}

function changeDescription(courseID) {
  var description = document.getElementById(`id-${courseID}`).value;
  fetch("/manager/courses/updateDescription", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      courseID: courseID,
      description: description,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then(() => {
      window.location.reload();
    })
    .catch((error) => {
      console.log(error);
    });
}

function showCourseDetails() {
  var details = document.getElementById("new-course-details");
  if (details.style.display === "none" || details.style.display === "") {
    details.style.display = "block";
  } else {
    details.style.display = "none";
  }
}

function saveCourse() {
  const name = document.getElementById("course-name").value;
  const description = document.getElementById("course-description").value;
  fetch("/manager/courses/addNewCourses", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      description: description,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then(() => {
      window.location.reload();
    })
    .catch((error) => {
      console.log(error);
    });
}

function getStudent() {
  var name = document.getElementById("name").value;
  var courseID = document.getElementById("course-id").value;
  fetch("/manager/students/getGrade", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      courseID: courseID,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then((data) => {
      if (Object.keys(data.student).length === 0 && data.student.constructor === Object) {
        document.getElementById("students-grades").innerHTML = `
    <h3>${name} doesn't learn this course</h3>`;
      } else {
        document.getElementById("students-grades").innerHTML = `
    <h3>${data.student.name}: ${data.student.grade}</h3>
    `;
      }
    })
    .catch((error) => console.log(error));
}

function getAllStudents() {
  fetch("manager/students/allStudents", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.message);
      }
      return response.json();
    })
    .then((data) => {
      const studentsContainer = document.getElementById("students-grades");
      document.getElementById("students-grades").innerHTML = ``;
      data.students.forEach((student) => {
        const card = document.createElement("div");
        card.className = "student-card";
        card.innerHTML = ` 
      <div class="card-body">
                <h3 class="card-title">${student.name}</h3>
                <h5>Number of Courses: ${student.number_of_courses}</h5>
                <h5>GPA: ${student.GPA}%</h5>
                <div class="buttons">
                  <button
                    type="button"
                    class="btn btn-outline-danger"
                    onclick="deleteUser(' ${student.id}')"
                  >
                    <i class="fa-solid fa-trash"></i>
                  </button>
                  <a
                    href="mailto:${student.email}"
                    class="btn btn-outline-primary"
                  >
                    <i class="fa-solid fa-envelope"></i>
                  </a>
                </div>
              </div>
      `;
        studentsContainer.appendChild(card);
      });
    })
    .catch((error) => {
      console.log("Error fetching students:", error);
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
