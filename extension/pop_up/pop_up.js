setTimeout(() => {
    let courses = []
    let courseList = document.querySelector("div.course-org-list");
    courseList = courseList.querySelectorAll(".course-id");
    for (let i = 0; i < courseList.length; i++) {
        const text = courseList[i].querySelector("span").innerText;
        courses.push(text);
    }
    const courseYear = courses[0].slice(10, 14);
    courses = courses.filter(element => element.slice(10, 14) === courseYear).map(e => e.slice(0, 8));
}, 5000);