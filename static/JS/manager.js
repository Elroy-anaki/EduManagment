function deleteTeacher(teacherID) {
  fetch("/manager/deleteUser", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      teacherID: teacherID,
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

