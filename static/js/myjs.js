function CheckEmail(str){
  var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
  if(!reg_email.test(str)) {
  return false;
  }
  else {
    return true;
  }
}

function login() {

  let userID = $("#userId").val();
  let userPW = $("#password").val();


  $.ajax({
    type: "POST",
    url: "/login_pro",
    data: { ID_give: userID, PW_give: userPW},
    success: function(response){
      console.log(response);
      if (response['result'] == 'success') {
          sessionStorage.setItem('my_access_token', response['access_token']);
          location.href = "/"

      } else {
          alert("아이디 또는 비밀번호를 다시 확인해주세요.");
          window.location.reaload();
      }
    }
  })
}

function join() {
  let userName = $("#name").val();
  let userId = $("#userID").val();
  let userPw = $("#userPW").val();
  let userEmail = $("#email").val();
  let id_info = $('#userIdInfo').text();

    if (userName == "" || userId == "" || userPw == "" || userEmail == "") {
      alert("빠짐없이 입력해주세요!")
    } else {     
      if (id_info == "" || id_info == "중복된 아이디입니다.") {
        $('#userIdInfo2').text("아이디 중복 확인 해주세요!")
      } else if(!CheckEmail(userEmail)){
        $('#userEmailInfo').text("올바르지 않은 이메일 형식입니다.")
        $("#email").val("")
    } else {
      $.ajax({
        
        type: "POST", 
        url: "/join_pro",
        data: { ID_give: userId, PW_give: userPw, Name_give: userName, Email_give: userEmail},
        success: function(response){
          console.log(response)
          if (response['result'] == 'success') {
            location.href = "/welcome";
          } else {
            alert("예기치 못한 오류가 발생했습니다. 다시 입력해주세요.")
          }
        }
      })
    }
  }
}


function idOverlap() {
    let userId = $("#userID").val();
    let info = $('#userIdInfo').text();
    $.ajax({
      type: "POST", 
      url: "/id_overlapping_confirm",
      data: {ID_give: userId},
      success: function(response){
        if (userId == "") {
          $('#userIdInfo').text("아이디를 입력해주세요.")
          $('#userIdInfo2').text("")
        } else if (response['result']=="success") {
          $('#userIdInfo').text("사용가능한 아이디입니다.")
          $('#userIdInfo2').text("")
        }
        else {
          $('#userIdInfo').text( "중복된 아이디입니다.")
          $('#userIdInfo2').text("")
          $("#userID").val("")
        }
      }
    })
}

function newidOverlap() {
  let userId = $("#userID").val();
  let info = $('newIdInfo').text();
  $.ajax({
    type: "POST", 
    url: "/id_overlapping_confirm",
    data: {ID_give: userId},
    success: function(response){
      console.log(response);
      if (sessionStorage.getItem('user_id') == userId) {
        $('#newIdInfo').text("원래 아이디입니다.")
        $('#newIdInfo2').text("")
      } else if (userId == "") {
        $('#newIdInfo').text("아이디를 입력해주세요.")
        $('#newIdInfo2').text("")
      } else if (response['result']=="success") {
        $('#newIdInfo').text("사용가능한 아이디입니다.")
        $('#userIdInfo2').text("")
      }
      else {
        $('#newIdInfo').text( "중복된 아이디입니다.")
        $('#newIdInfo2').text("")
        $("#newIdInfo").val("")
      }
    }
  })
}

function getModification() {
    let userToken = localStorage.getItem('my_access_token');
    $.ajax({
      type: "POST", 
      url: "/modification",
      data: {'token_give': userToken},
      success: function(response){
        console.log(response)
        if (response['result']=="success") {
          location.href = "/modication_form";
          sessionStorage.setItem('user_id', response['user_id'])
          sessionStorage.setItem('user_name', response['user_name'])
          sessionStorage.setItem('user_email', response['user_email'])
        }
        else {
          alert('다시로그인해주세요.')
          location.href = "/login";
        }
      }
    })
 }

 function newPwOverlap() {
  let newPw = $("#userPW").val();
  let newPwConfirm = $('#newUserPw').val();
  console.log(newPw, newPwConfirm)
  if (newPw == newPwConfirm) {
    $('#newPwInfo').text("비밀번호가 일치합니다.")
    $('#userIdInfo2').text("")
  } else {
    $('#newPwInfo').text("비밀번호가 다릅니다.")
    $('#userIdInfo2').text("")
  }
}


function modification_complete() {
    let oridinalId = sessionStorage.getItem("user_id");
    let userName = $("#name").val();
    let userId = $("#userID").val();
    let userPw = $("#userPW").val();
    let userEmail = $("#email").val();
    let id_info = $('#newIdInfo').text();
    let pw_info = $('#newPwInfo').text();
  
      if (userName == "" || userId == "" || userPw == "" || userEmail == "") {
        alert("빠짐없이 입력해주세요!")
      } else {     
        if (id_info == "" || id_info == "중복된 아이디입니다.") {
          $('#userIdInfo2').text("아이디 중복 확인 해주세요!")
        } else if(pw_info == "" || pw_info == "비밀번호가 다릅니다.") {
          $('#userPwInfo2').text("비밀번호 일치 확인 해주세요!")
        } else if(!CheckEmail(userEmail)){
          $('#userEmailInfo').text("올바르지 않은 이메일 형식입니다.")
          $("#email").val("")
      } else {
        $.ajax({
          type: "POST", 
          url: "/modification_complete",
          data: {Oridinal_id: oridinalId, ID_give: userId, PW_give: userPw, Name_give: userName, Email_give: userEmail},
          success: function(response){
            console.log(response)
            if (response['result'] == 'success') {
              alert("수정이 완료되었습니다!")
              location.href = "/";
            } else {
              alert("예기치 못한 오류가 발생했습니다. 다시 입력해주세요.")
            }
          }
        })
      }
    }
}
