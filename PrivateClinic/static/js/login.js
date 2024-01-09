$(document).ready(function() {
    //Loading
    setInterval(function() {
        $('.loading').fadeOut();
    }, 1000);
    //Sign in
    $('.signIn-form .last-question span').click(function() {
        $('.active').addClass('di-vao-ben-trai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-trai').removeClass('di-vao-ben-trai').removeClass('active');
        })
        $('#signUp').addClass('active').addClass('hien-ra-ben-phai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-phai').removeClass('hien-ra-ben-phai');
        });
    });
    $('.signIn-choose span').click(function() {
        $('.active').addClass('di-vao-ben-phai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-phai').removeClass('di-vao-ben-phai').removeClass('active');
        })
        $('#forgot-pw').addClass('active').addClass('hien-ra-ben-trai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-trai').removeClass('hien-ra-ben-trai');
        });
    });
    //Sign up
    $('.signUp-form .main-btn span').click(function() {
        alert('Bạn đã đăng ký thành công! Hãy đăng nhập để sự dụng dịch vu...');
        $('.active').addClass('di-vao-ben-phai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-phai').removeClass('di-vao-ben-phai').removeClass('active');
        })
        $('#signIn').addClass('active').addClass('hien-ra-ben-trai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-trai').removeClass('hien-ra-ben-trai');
        });
    })
    $('.signUp-form .last-question span').click(function() {
        $('.active').addClass('di-vao-ben-phai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-phai').removeClass('di-vao-ben-phai').removeClass('active');
        })
        $('#signIn').addClass('active').addClass('hien-ra-ben-trai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-trai').removeClass('hien-ra-ben-trai');
        });
    })
    //Forgot password
    $('.forgot-form .main-btn span').click(function() {
        alert('Đặt lại mật khẩu thành công!');
        $('.active').addClass('di-vao-ben-trai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-trai').removeClass('di-vao-ben-trai').removeClass('active');
        })
        $('#signIn').addClass('active').addClass('hien-ra-ben-phai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-phai').removeClass('hien-ra-ben-phai');
        });
    });
    $('.forgot-form .last-question > div:first-child span').click(function() {
        $('.active').addClass('di-vao-ben-trai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-trai').removeClass('di-vao-ben-trai').removeClass('active');
        })
        $('#signIn').addClass('active').addClass('hien-ra-ben-phai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-phai').removeClass('hien-ra-ben-phai');
        });
    });
    $('.forgot-form .last-question > div:last-child span').click(function() {
        $('.active').addClass('di-vao-ben-phai').one('webkitAnimationEnd',() => {
            $('.di-vao-ben-phai').removeClass('di-vao-ben-phai').removeClass('active');
        })
        $('#signUp').addClass('active').addClass('hien-ra-ben-trai').one('webkitAnimationEnd',() => {
            $('.hien-ra-ben-trai').removeClass('hien-ra-ben-trai');
        });
    })
});