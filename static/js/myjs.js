function CheckEmail(str){
  var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
  if(!reg_email.test(str)) {
  return false;
  }
  else {
    return true;
  }
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
      data: {ID_give: userId}, // 데이터를 주는 방법
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
    data: {ID_give: userId}, // 데이터를 주는 방법
    success: function(response){
      if (userId == "") {
        $('#newIdInfo').text("아이디를 입력해주세요.")
        $('#newIdInfo2').text("")
      } else if (response['result']=="success") {
        $('#userIdInfo').text("사용가능한 아이디입니다.")
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
    let userToken = sessionStorage.getItem('my_access_token');
    $.ajax({
      type: "POST", 
      url: "/modification",
      data: {'token_give': userToken},
      success: function(response){
        console.log(response)
        if (response['result']=="success") {
          $('#name').
            location.href = "/modication_form";
        }
        else {
          alert('다시로그인해주세요.')
          location.href = "/login";
        }
      }
    })
 }
