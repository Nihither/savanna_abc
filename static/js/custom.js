// document ready section

$(document).ready(function () {

    var timeout;

    get_teacher_list();
    get_student_list();
    get_subjects_per_teacher_list();

    $('.date_in_calendar').click(function (e) { 
        e.preventDefault();
        let teacher_id = $(this).attr('teacher');
        let year = $(this).attr('year');
        let month = $(this).attr('month');
        let day = $(this).attr('day');
        let url = `/teacher/${teacher_id}/${year}/${month}/${day}/`;
        $.get(url, function (data, textStatus, jqXHR) {
                $('#classes_per_day').html(data);
            },
            "html"
        );
    });

    // teacher section

    $('#show_archive_teacher_list').click(function (e) { 
        e.preventDefault();
        get_teacher_archive_list();
        $(this).addClass('active');
        $('#show_active_teacher_list').removeClass('active');
    });

    $('#show_active_teacher_list').click(function (e) { 
        e.preventDefault();
        get_teacher_list();
        $(this).addClass('active');
        $('#show_archive_teacher_list').removeClass('active');
    });

    $('#search_results_teacher_input').keyup(function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            get_search_results_teacher();
        }, 500);
    });

    $('#add_teacher').click(function (e) { 
        e.preventDefault();
        let url = '/teacher/add/';
        $("#index_page_modal_title").text('Добавить преподавателя');
        $.get(url, function (data, textStatus, jqXHR) {
                $('#index_page_modal_body').html(data);
                $('#index_page_modal').modal('toggle');
            },
            "html"
        );
    });

    $('#delete_teacher').click(function (e) { 
        e.preventDefault();
        let url = 'delete/';
        let form_data = $(this).children('input').serialize();
        $.ajax({
            type: "post",
            url: url,
            data: form_data,
            success: function (response) {
                trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
                setTimeout(() => {
                    location.href = "/";
                }, (delay+1000));
            },
            error: function (response) {
                trigger_alert(alert_text=response.responseText, alert_status='alert-warning', delay=2000);
            }
        });
    });

    $('#archive_teacher').click(function (e) { 
        e.preventDefault();
        let url = 'archive/';
        let form_data = $(this).children('input').serialize();
        $.ajax({
            type: "post",
            url: url,
            data: form_data,
            success: function (response) {
                trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
                setTimeout(() => {
                    location.reload();
                }, 2000);
            },
            error: function (response) {
                trigger_alert(alert_text=response.responseText, alert_status='alert-warning', delay=2000);
            }
        });
    });

    $('#set_available_timestamps').click(function (e) { 
        e.preventDefault();
        let url = 'timestamps/'
        $("#teacher_page_modal_title").text('Изменить окна');
        $.get(url, function (data, textStatus, jqXHR) {
                $('#teacher_page_modal_body').html(data);
                $('#teacher_page_modal').modal('toggle');
            },
            "html"
        );
    });

    $('#assign_student_to_teacher').click(function (e) { 
        e.preventDefault();
        let url = 'student/assign/';
        $("#teacher_page_modal_title").text('Назначить студента');
        $.get(url, function (data, textStatus, jqXHR) {
                $('#teacher_page_modal_body').html(data);
                $('#teacher_page_modal').modal('toggle');
            },
            "html"
        );
    });

    $('#reject_student_to_teacher').click(function (e) { 
        e.preventDefault();
        let url = 'student/reject/';
        $("#teacher_page_modal_title").text('Удалить студента');
        $.get(url, function (data, textStatus, jqXHR) {
                $('#teacher_page_modal_body').html(data);
                $('#teacher_page_modal').modal('toggle');
            },
            "html"
        );
    });

    // student section

    $('#show_archive_student_list').click(function (e) { 
        e.preventDefault();
        get_student_archive_list();
        $(this).addClass('active');
        $('#show_active_student_list').removeClass('active');
    });

    $('#show_active_student_list').click(function (e) { 
        e.preventDefault();
        get_student_list();
        $(this).addClass('active');
        $('#show_archive_student_list').removeClass('active');
    });

    $('#search_results_student_input').keyup(function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            get_search_results_student();
        }, 500);
    });

    $('#add_student').click(function (e) { 
        e.preventDefault();
        let url = '/student/add/';
        $("#index_page_modal_title").text('Добавить преподавателя');
        $.get(url, function (data, textStatus, jqXHR) {
                $('#index_page_modal_body').html(data);
                $('#index_page_modal').modal('toggle');
            },
            "html"
        );
    });

    $('#delete_student').click(function (e) { 
        e.preventDefault();
        let url = 'delete/';
        let form_data = $(this).children('input').serialize();
        $.ajax({
            type: "post",
            url: url,
            data: form_data,
            success: function (response) {
                trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
                setTimeout(() => {
                    location.href = "/";
                }, (delay+1000));
            },
            error: function (response) {
                trigger_alert(alert_text=response.responseText, alert_status='alert-warning', delay=2000);
            }
        });
    });

    $('#archive_student').click(function (e) { 
        e.preventDefault();
        let url = 'archive/';
        let form_data = $(this).children('input').serialize();
        $.ajax({
            type: "post",
            url: url,
            data: form_data,
            success: function (response) {
                trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
                setTimeout(() => {
                    location.reload();;
                }, 2000);
            },
            error: function (response) {
                trigger_alert(alert_text=response.responseText, alert_status='alert-warning', delay=2000);
            }
        });
    });

    // other section

    $('#teacher_page_modal_body').on('click', '.schedule_cell_checkbox', function () {
        $(this).toggleClass('info');
    });

    // how to use jq on dinamic objects
    // $('#add_person_body').on('click', '#add_teacher_btn', function () {
    //     console.log('click');
    // });

});

// end of document ready section

// functions section

// teachers

function get_teacher_list() {
    $.get("/teacher/list/", function (data, textStatus, jqXHR) {
            $('#teacher_list_body').html(data);
        },
        "html"
    );
};

function get_teacher_archive_list() {
    $.get("/teacher/list/archive/", function (data, textStatus, jqXHR) {
            $('#teacher_list_body').html(data);
        },
        "html"
    );
};

function get_search_results_teacher() {
    let data = $('#search_results_teacher_form').serialize();
    $.get("/teacher/search/", data, function (data, textStatus, jqXHR) {
            $('#teacher_list_body').html(data);
        },
        "html"
    );
};

function get_subjects_per_teacher_list() {
    $.get("students/", function (data, textStatus, jqXHR) {
            $('#students_list_per_teacher_panel').html(data);
        },
        "html"
    );
};

function add_teacher() {
    let form_data = $('#add_teacher_form').serialize();
    $.ajax({
        type: "post",
        url: "/teacher/add/",
        data: form_data,
        success: function (response) {
            $('#index_page_modal').modal('toggle');
            get_teacher_list();
            trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
        },
        error: function (response) {
            $('#index_page_modal_body').html(response.responseText);
        }
    });
};

function assign_student_to_teacher() {
    let url = 'student/assign/'
    let form_data = $('#assign_student_to_teacher_form').serialize();
    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (response) {
            $('#teacher_page_modal').modal('toggle');
            get_subjects_per_teacher_list();
            trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
        },
        error: function (response) {
            $('#teacher_modal_body').html(response.responseText);
        }
    });
};

function reject_student_to_teacher() {
    let url = 'student/reject/'
    let form_data = $('#reject_student_to_teacher_form').serialize();
    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        success: function (response) {
            $('#teacher_page_modal').modal('toggle');
            get_subjects_per_teacher_list();
            trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
        },
        error: function (response) {
            $('#teacher_modal_body').html(response.responseText);
        }
    });
};

// students

function get_student_list() {
    $.get("/student/list/", function (data, textStatus, jqXHR) {
            $('#student_list_body').html(data);
        },
        "html"
    );
};

function get_student_archive_list() {
    $.get("/student/list/archive", function (data, textStatus, jqXHR) {
            $('#student_list_body').html(data);
        },
        "html"
    );
};

function get_search_results_student() {
    let data = $('#search_results_student_form').serialize();
    $.get("/student/search/", data,
        function (data, textStatus, jqXHR) {
            $('#student_list_body').html(data);
        },
        "html"
    );
};

function add_student(params) {
    let form_data = $('#add_student_form').serialize();
    $.ajax({
        type: "post",
        url: "/student/add/",
        data: form_data,
        success: function (response) {
            $('#index_page_modal').modal('toggle');
            get_student_list();
            trigger_alert(alert_text=response, alert_status='alert-success', delay=2000);
        },
        error: function (response) {
            $('#index_page_modal_body').html(response.responseText);
        }
    });
};

// alerts

function trigger_alert(alert_text, alert_status, delay) {
    show_alert(alert_text=alert_text, alert_status=alert_status);
    setTimeout(() => {
        hide_alert();
    }, delay);
};

function show_alert(alert_text, alert_status) {
    const alert_body = `<div class="alert ${alert_status}" id="alert_content" role="alert">
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <p id="add_person_status">${alert_text}</p>
                        </div>`;
    $('#alert_block').html(alert_body);
};

function hide_alert() {
    $('#alert_content').alert('close');
};

// end of functin section