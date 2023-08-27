const url = chrome.runtime.getURL('course_data.json');
let data = [];
fetch(url)
    .then((response) => response.json())
    .then((json) => data = json.courses);


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
    const result = data.filter(cool => courses.some(name => cool.course === name))
    console.log(result)
}, 5000);


//Eugene's code Waiting for clean up
// let courseList = undefined;
// let sameSemCoursesShort = undefined;
// setTimeout(() => {
//     courseList = document.querySelector("div.course-org-list");
//     courseList = courseList.querySelectorAll(".course-id");
//     for (let i = 0; i < courseList.length; i++) {
//         courseList[i].style.color = "red";
//       }
//      const courses =  Array.from(courseList, item => item.innerText);
//      const sameSemCourses = courses.filter(course => courses[0].slice(10,15) === course.slice(10,15));
//      const sameSemCoursesShort = sameSemCourses.map(course => course.slice(0,8));

// const coursesSECAT = fetch(chrome.runtime.getURL('course_data.json'))
//     .then(data => data.json())
//     .then(data => data.courses)
//     .then(data => data.filter(elem => sameSemCoursesShort
//     .includes(elem.course)))
//     .then(data => console.log(data));


// }, 5000);


/* 
async function readCache(filePath) {
    try {
        const data = await fs.readFile(filePath);
        return data;
    }
    catch (error) {
        return undefined;
    }
}

async function readJSONFromCache(filePath) {
    return JSON.parse(await readCache(filePath));
}
 */

