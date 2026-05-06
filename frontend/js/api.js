const API_BASE = '';

const API = {
    async get(url) {
        try {
            const response = await fetch(API_BASE + url);
            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: '请求失败' }));
                throw new Error(error.detail || '请求失败');
            }
            return await response.json();
        } catch (error) {
            console.error('GET请求错误:', error);
            throw error;
        }
    },

    async post(url, data) {
        try {
            const response = await fetch(API_BASE + url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: '请求失败' }));
                throw new Error(error.detail || '请求失败');
            }
            return await response.json();
        } catch (error) {
            console.error('POST请求错误:', error);
            throw error;
        }
    },

    async put(url, data) {
        try {
            const response = await fetch(API_BASE + url, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: '请求失败' }));
                throw new Error(error.detail || '请求失败');
            }
            return await response.json();
        } catch (error) {
            console.error('PUT请求错误:', error);
            throw error;
        }
    },

    async delete(url) {
        try {
            const response = await fetch(API_BASE + url, {
                method: 'DELETE'
            });
            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: '删除失败' }));
                throw new Error(error.detail || '删除失败');
            }
            return await response.json();
        } catch (error) {
            console.error('DELETE请求错误:', error);
            throw error;
        }
    }
};

const StudentAPI = {
    list: (page = 1, size = 10) => API.get(`/students?page=${page}&size=${size}`),
    get: (stuId) => API.get(`/students/${stuId}`),
    search: (stuId, stuName, classId) => {
        let url = `/students/${stuId}`;
        const params = [];
        if (stuName) params.push(`stu_name=${stuName}`);
        if (classId) params.push(`class_id=${classId}`);
        if (params.length > 0) url += '?' + params.join('&');
        return API.get(url);
    },
    create: (data) => API.post('/students', data),
    update: (stuId, data) => API.put(`/students/${stuId}`, data),
    delete: (stuId) => API.delete(`/students/${stuId}`)
};

const CourseAPI = {
    list: (page = 1, pageSize = 5, courseName = '') => {
        let url = `/api/course/courses?page=${page}&page_size=${pageSize}`;
        if (courseName) url += `&course_name=${encodeURIComponent(courseName)}`;
        return API.get(url);
    },
    get: (courseId) => API.get(`/api/course/course/${courseId}`),
    create: (data) => API.post('/api/course/courses', data),
    update: (courseId, data) => API.put(`/api/course/course/update/${courseId}`, data),
    delete: (courseId) => API.delete(`/api/course/course/delete/${courseId}`),
    restore: (courseId) => API.put(`/api/course/course/restore/${courseId}`)
};

const ScoreAPI = {
    list: () => API.get('/score/get_all'),
    get: (stuId) => API.get(`/score/${stuId}`),
    create: (data) => API.post('/score/', data),
    update: (stuId, testNum, examCourseId, data) => API.put(`/score/update?stu_id=${stuId}&test_num=${testNum}&exam_course_id=${examCourseId}`, data),
    delete: (stuId, testNum, examCourseId) => API.delete(`/score/delete?stu_id=${stuId}&test_num=${testNum}&exam_course_id=${examCourseId}`)
};

const ClassAPI = {
    list: () => API.get('/classes/classes'),
    get: (classId) => API.get(`/classes/classes/${classId}`),
    create: (data) => API.post('/classes/classes', data),
    update: (classId, data) => API.put(`/classes/${classId}`, data),
    delete: (classId) => API.delete(`/classes/classes/${classId}`),
    students: (classId) => API.get(`/classes/classes/${classId}/students`)
};

const DepartmentAPI = {
    list: (page = 1, pageSize = 5, departmentName = '') => {
        let url = `/api/department/departments?page=${page}&page_size=${pageSize}`;
        if (departmentName) url += `&department_name=${encodeURIComponent(departmentName)}`;
        return API.get(url);
    },
    get: (deptId) => API.get(`/api/department/department/${deptId}`),
    create: (data) => API.post('/api/department/departments', data),
    update: (deptId, data) => API.put(`/api/department/department/update/${deptId}`, data),
    delete: (deptId) => API.delete(`/api/department/department/delete/${deptId}`),
    restore: (deptId) => API.put(`/api/department/department/restore/${deptId}`)
};

const EmployeeAPI = {
    list: () => API.get('/employee/employees/employee/list'),
    search: (name) => API.get(`/employee/employees/search?name=${encodeURIComponent(name)}`),
    get: (id) => API.get(`/employee/employees/${id}`),
    create: (data) => API.post('/employee/employees/create_emp', data),
    update: (id, data) => API.put(`/employee/employees/${id}`, data),
    delete: (id) => API.delete(`/employee/employees/${id}`)
};

const EmploymentAPI = {
    list: () => API.get('/employment/'),
    getByStudent: (stuId) => API.get(`/employment/students/${stuId}`),
    getByClass: (classId) => API.get(`/employment/class/${classId}`),
    create: (data) => API.post('/employment/', data),
    update: (stuId, data) => API.put(`/employment/students/${stuId}`, data),
    delete: (stuId) => API.delete(`/employment/students/${stuId}`)
};

const StatsAPI = {
    highScore: () => API.get('/statistics/high_score'),
    lowScore: () => API.get('/statistics/low_score'),
    avgScore: () => API.get('/statistics/avg_score'),
    courseCount: () => API.get('/statistics/statistics/count_course'),
    courseStudents: () => API.get('/statistics/statistics/count_students_by_course'),
    deptCount: () => API.get('/statistics/statistics/count_department'),
    deptEmployees: () => API.get('/statistics/statistics/count_employees_by_department'),
    over30: () => API.get('/statistics/get/over30'),
    classStat: () => API.get('/statistics/stat/class'),
    classCount: () => API.get('/statistics/statistics/classes/count'),
    classAvgScore: (testNum) => API.get(`/statistics/statistics/classes/average-score${testNum ? '?考试序次=' + testNum : ''}`),
    classAvgDuration: () => API.get('/statistics/statistics/classes/average-employment'),
    empStats: () => API.get('/statistics/employees/stat/statistics'),
    empPosition: () => API.get('/statistics/employees/stat/position'),
    top5Salary: () => API.get('/statistics/statistics/top5-salary'),
    studentDuration: () => API.get('/statistics/statistics/student_offer'),
    classAvgDuration: () => API.get('/statistics/statistics/avg_student_offer')
};
