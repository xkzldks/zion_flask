        $(document).ready(function () {
                showReview();
                getUserAuth();
            });
        let result = '';
        let copySen = '';
        function getUserAuth(){
                $.ajax({
                        type: "GET",
                        url: "/getUserAuth",
                        data: {},
                        success: function (response) {
                            let auth = response['msg']
                            console.log(auth);
                            if(auth == ''){
                                var txt = "<div>*비로그인*</div>"
                                document.getElementById("userAuth").innerHTML += txt;
                            }
                            else if(auth == 1){
                                var txt = "<div>*관리자계정*</div><br><div style='text-align: center;'><a href= checkq  >>> QR출석체크 <<</a></div>"
                                document.getElementById("userAuth").innerHTML += txt;
                            }
                            else if(auth == 2){
                                var txt = "<div>*게스트계정*</div>"
                                document.getElementById("userAuth").innerHTML += txt;
                            }
                        }
                    })
            }
        function getCheckboxValue(){
                let group = Object.values(getGroupList);;
                console.log(group);
                for(let i = 0; i < group.length; i++){
                    let c = 'input[name='+ getGroupList[i]['조 이름']+']:checked';
                    const s = document.querySelectorAll(c);

                    s.forEach((el) => {
                                result += el.value + ' ';
                    });
                }
                console.log(result);


                let c = "input[name='미분류']:checked";
                const s = document.querySelectorAll(c);

                s.forEach((el) => {
                            result += el.value + ' ';
                });
                console.log(result);
                alert('선택된 인원\n'+result);
                document.getElementById('result').innerText = result;
        }
        function getDb(){
             if(confirm("명단을 저장하시겠습니까?") == true){
                 getCheckboxValue();
                    if (document.getElementById('result').innerText == ""){
                        if(confirm("체크가 되지않았지만 명단을 저장하시겠습니까?") == true){
                            chulCheck();
                        }
                        else{
                            document.getElementById('result').innerText = ""
                            result = ""
                        }
                    }
                    else{
                        chulCheck();
                    }
                }
            }

        function chulCheck(){
            var test1 = document.getElementById('checkboxDateC');
                if($(test1).is(":checked") == true){
                    title = $('#title').val()
                }
                else{
                    date = new Date();
                    month = date.getMonth() + 1;
                    day = date.getDate();
                    if (month <= 9){
                        month = "0"+String(month);
                    }
                    if(day <=9){
                        day = "0"+String(day);
                    }


                    title = month+String(day);
                }

            $.ajax({
                    type: "POST",
                    url: "/chulCheck",
                    data: {title_give:title},
                    success: function (response) {
                        let check = response['check']
                        let title = check['title']
                        let review = check['review']
                        console.log(check);
                        if(check == ''){
                            dateCheck();
                        }
                        else if(check == 'false'){
                            alert(response["check"]);
                            document.getElementById('result').innerText = ""
                        }
                        else{
                            if(confirm("현재 저장된 데이터: "+title + review +"\n저장하시면 이 데이터는 삭제되고 새로운 데이터가 저장됩니다. \n저장하시겠습니까?") == true){
                                dateCheck();
                            }
                            else{
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                        }
                    }
                })
            }

        function makeReview() {
                var test1 = document.getElementById('checkboxDateC');
                if($(test1).is(":checked") == true){
                    title = $('#title').val()
                }
                else{
                    date = new Date();
                    month = date.getMonth() + 1;
                    day = date.getDate();
                    if (month <= 9){
                        month = "0"+String(month);
                    }
                    if(day <=9){
                        day = "0"+String(day);
                    }

                    title = month+String(day);
                }
                let review = document.getElementById('result').innerText
                if(title != "초기화"){
                        $.ajax({
                            type: "POST",
                            url: "/review",
                            data: {title_give:title, review_give:review},
                            success: function (response) {
                            if(response['False'] == 'False'){
                                alert("로그인이 필요한 서비스입니다.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                    })
                }
                else{
                    alert("잘못된 접근입니다");
                }

        }

        function dateCheck(){
        var test1 = document.getElementById('checkboxDateC');
            if($(test1).is(":checked") != true || $(title).val() != ""){
                makeReview()
            }
            else{
                alert("날짜를 확인해주세요");
                document.getElementById('result').innerText = ""
                result = ""
            }
        }

        function getCheckDB(){
        var test1 = document.getElementById('checkboxDateC');
                if($(test1).is(":checked") == true){
                    title = $('#title').val()
                }
                else{
                    date = new Date();
                    month = date.getMonth() + 1;
                    day = date.getDate();
                    if (month <= 9){
                        month = "0"+String(month);
                    }
                    if(day <=9){
                        day = "0"+String(day);
                    }


                    title = month+String(day);


                }
                let review = document.getElementById('result').innerText

            if(title == ""){
                alert("삭제할 명단의 날짜를 입력하세요");
                document.getElementById('result').innerText = ""
                result = ""
            }
            else if(title == "초기화"){
                if(confirm("!!!경고!!!\n※모든 출석기록을 삭제하시겠습니까?\n※삭제하기전 이전 데이터는 백업부탁드립니다.\n※그래프탭에서 오늘날짜기준 csv다운")==true){
                    if(confirm("※!!초기화 후 날짜별로 저장된 출석명단이 전체 삭제됩니다.\n한번 더 확인을 눌러 초기화를 진행해주세요!!")==true){
                        $.ajax({
                                type: "POST",
                                url: "/dbReset",
                                data: {},
                                success: function (response) {
                                        if(response['False'] == 'False'){
                                            alert("로그인이 필요한 서비스입니다.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else if(response['False'] == 'Auth'){
                                            alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else{
                                            alert(response["msg"]);
                                            window.location.reload();
                                        }
                                    }
                            })
                    }
                }
            }
            else{
                if(confirm(title+" 명단을 삭제하시겠습니까?") == true){
                       $.ajax({
                                type: "POST",
                                url: "/dbDel",
                                data: {title_give:title},
                                success: function (response) {
                                        if(response['False'] == 'False'){
                                            alert("로그인이 필요한 서비스입니다.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else if(response['False'] == 'Auth'){
                                            alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else{
                                            alert(response["msg"]);
                                            window.location.reload();
                                        }
                                    }
                            })
                       if (error ) {
                            return false;
                       }
                    }
                else{
                    document.getElementById('result').innerText = ""
                    result = ""
                }
            }
            }
        function getCheckAddPerson(){
            getCheckboxValue();
            var test1 = document.getElementById('checkboxDateC');
                if($(test1).is(":checked") == true){
                    title = $('#title').val()
                }
                else{
                    date = new Date();
                    month = date.getMonth() + 1;
                    day = date.getDate();
                    if (month <= 9){
                        month = "0"+String(month);
                    }
                    if(day <=9){
                        day = "0"+String(day);
                    }


                    title = month+String(day);
                }
                if(title == "" ||( document.getElementById('result').innerText == "")){
                    alert("추가할 명단의 날짜와 해당 인원을 확인하세요");
                    document.getElementById('result').innerText = ""
                    result = ""
                    }
                else{
                    if(confirm(title + " 해당 인원의 출석기록을 추가하시겠습니까?") == true){
                        let review = document.getElementById('result').innerText
                               $.ajax({
                                        type: "POST",
                                        url: "/personAdd",
                                        data: {title_give:title, new_give:review},
                                        success: function (response) {
                                            if(response['False'] == 'False'){
                                                alert("로그인이 필요한 서비스입니다.");
                                                document.getElementById('result').innerText = ""
                                                result = ""
                                            }
                                            else if(response['False'] == 'Auth'){
                                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                                document.getElementById('result').innerText = ""
                                                result = ""
                                            }
                                            else{
                                                alert(response["msg"]);
                                                window.location.reload();
                                            }
                                        }
                               })
                    }
                    else{
                         document.getElementById('result').innerText = ""
                         result = ""
                    }
                }

            }
        function getCheckDelPerson(){
            getCheckboxValue();
            var test1 = document.getElementById('checkboxDateC');
                if($(test1).is(":checked") == true){
                    title = $('#title').val()
                }
                else{
                    date = new Date();
                    month = date.getMonth() + 1;
                    day = date.getDate();
                    if (month <= 9){
                        month = "0"+String(month);
                    }
                    if(day <=9){
                        day = "0"+String(day);
                    }


                    title = month+String(day);
                }
            if(title == "" ||( document.getElementById('result').innerText == "")){
                    alert("삭제할 명단의 날짜와 해당 인원을 확인하세요");
                    document.getElementById('result').innerText = ""
                    result = ""
                }
            else{
                if(confirm($('#title').val() + " 해당 인원의 출석기록을 삭제하시겠습니까?") == true){
                    let review = document.getElementById('result').innerText
                           $.ajax({
                                    type: "POST",
                                    url: "/personDel",
                                    data: {title_give:title, new_give:review},
                                    success: function (response) {
                                        if(response['False'] == 'False'){
                                            alert("로그인이 필요한 서비스입니다.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else if(response['False'] == 'Auth'){
                                            alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                            document.getElementById('result').innerText = ""
                                            result = ""
                                        }
                                        else{
                                            alert(response["msg"]);
                                            window.location.reload();
                                        }
                                    }
                           })
                }
                else{
                     document.getElementById('result').innerText = ""
                     result = ""
                }
            }
        }

        function checkCopy() {
            var test1 = document.getElementById('checkboxDateC');
                    if($(test1).is(":checked") == true){
                        title = $('#title').val()
                    }
                    else{
                        date = new Date();
                        month = date.getMonth() + 1;
                        day = date.getDate();
                        if (month <= 9){
                            month = "0"+String(month);
                        }
                        if(day <=9){
                            day = "0"+String(day);
                        }
                        title = month+String(day);
                    }
            if(title == ""){
                    alert("결과복사할 날짜를 확인하세요");
                    }
                else{
                    if(confirm(title+ " 해당 날짜의 결과를 복사하시겠습니까?") == true){
                           $.ajax({
                                    type: "POST",
                                    url: "/copyResult",
                                    data: {title_give:title},
                                    success: function () {
                                    getCopy();
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                    }
                        })
                    }
                    else{
                         document.getElementById('result').innerText = ""
                         result = ""
                    }
                }
            }
        function getCopy() {
                alert('결과복사 시작');
                $.ajax({
                      type: "GET",
                      url: "/copyResult",
                      data: {},
                      success: function (response) {
                          let reviews = response['review']
                          alert(reviews);
                          copyToClipboard(reviews);
                      }
                    })
            }
        function copyToClipboard(str) {
            var tempElement = document.createElement("textarea");
            document.body.appendChild(tempElement);
            tempElement.value = str;
            tempElement.select();
            document.execCommand('copy');
            document.body.removeChild(tempElement);
        }

        function graphCalc(){
            alert(document.getElementById("startDay").value());
        }
        function showReview() {
            getGroup()
                $.ajax({
                    type: "GET",
                    url: "/review",
                    data: {},
                    success: function (response) {
                        let reviews = response['all_reviews']
                        for (let i = 0; i < reviews.length; i++){
                            let year = reviews[i]['year']
                            let title = reviews[i]['title']
                            let review = reviews[i]['review']
                            let count = reviews[i]['count']
                            let temp_html = "<tr>"+
                                                "<td class = 'tdz' style='text-align : center;'>"+year+"</td>"+
                                                "<td href = '#' id = "+title+" onclick = getChul("+Number(title)+") class = 'tdz' style='text-align : center; color: olivedrab; text-decoration: underline;'>"+title+"</td>"+
                                                "<td class = 'tdz' style= 'text-align : center; word-break: keep-all;'>"+review+"</td>"+
                                                "<td class = 'tdz' style='text-align : center;'>"+count+"</td>"+
                                            "</tr>"
                            $('#reviews-box').append(temp_html)
                        }
                    }
                })
            }
        function getChul(a){
            err = '';
            errV = 0;
            $(":checkbox").prop("checked",false);
            $("#checkboxDateC").prop("checked",true);
            $('#title').attr("disabled",false);

            if(a<1000){
                a = "0"+String(a);
            }
            $('#title').val(a);
            console.log(a);
            $.ajax({
                  type: "POST",
                  url: "/copyResult",
                  data: {title_give:a},
                  success: function (response) {
                      console.log(response);
                      let review = response['review']
                      const reviews = review[0]['review'].split(' ');
                      for(let i = 1; i < reviews.length; i++){
                        try{
                            document.getElementById(reviews[i]).checked = true;
                        }catch(e){
                            err += reviews[i] + ' ';
                            errV += 1;
                        }
                      }
                      alert('##명단불러오기##\n '+ err + errV +'명 제외\n ' + (reviews.length -1 - errV) + '명 불러오기 성공!');
                  }

              })
        }
        function createCheckBox(){
            $.ajax({
                  type: "GET",
                  url: "/getDB",
                  data: {},
                  success: function (response) {
                      dbP = response['dbP']
                      let dbG = response['dbG']
                      console.log(dbP);
                      console.log(dbG);
                      document.getElementById("txtPanelAddCheckbox").innerHTML = "";
                      var t = "<div style ='text-align : center';>시온전체명단</div>";
                      document.getElementById("txtPanelAddCheckbox").innerHTML += t;

                      for(let i = 0; i < dbG.length; i++){
                         var txt = "<span style='line-height:20%'><br></span><div class = 'item' id ="+dbG[i]['조 이름']+">&nbsp;"+dbG[i]['조 이름']+"<br></div>"
                         document.getElementById("txtPanelAddCheckbox").innerHTML += txt;
                      }
                      console.log(dbP.length);
                      for(let n = 0; n < dbP.length; n++){
                         var txt = "<label><input type = 'checkbox' class='item' onclick='getCheckboxInfo(event)' id =  "+dbP[n]['이름']+" name = '" + dbP[n]['조']+ "'  value = '" + dbP[n]['이름'] + "'>&nbsp;"  + dbP[n]['이름'] + "&nbsp;</label>";
                         document.getElementById(dbP[n]['조']).innerHTML += txt;
                      }
                      getNotSetGroup()
                  }

              })
           }
        function getNotSetGroup(){
            $.ajax({
                  type: "GET",
                  url: "/getNotsetGroup",
                  data: {},
                  success: function (response) {
                      dbNSP = response['dbP']
                      document.getElementById("txtPanelAddNotGroupSet").innerHTML = "";
                      for (let i = 0; i < dbNSP.length+1; i++){
                            if(i == 0){
                                    var txt = "<br><hr style='border: solid 2px brown;'>"+'미분류 그룹 (※ 미분류 그룹에 인원이 있을시, 그래프 탭의 조별 출석률, 나이별 출석률 사용이 불가능합니다. 다른 조로 편성바랍니다.)' + "<br><label><input onclick='getNSGCheckboxInfo(event)' type = 'checkbox' name = '" + "미분류" + "'  value = '" + dbNSP[i]['이름'] + "'> "  + dbNSP[i]['이름'] + "</label> ";
                                    document.getElementById("txtPanelAddNotGroupSet").innerHTML += txt;
                            }
                            else if(i != dbNSP.length){
                                var txt = "<label><input onclick='getNSGCheckboxInfo(event)' type = 'checkbox' name = '" + "미분류"+ "'id = '" + dbNSP[i]['이름'] + "'  value = '" + dbNSP[i]['이름'] + "'> "  + dbNSP[i]['이름'] + "</label> ";
                                document.getElementById("txtPanelAddNotGroupSet").innerHTML += txt;
                            }
                            else{
                                var txt = "<br><a href='#'  class= 'myButtonDGroup' onclick='delMultiPeopleDB()'>인원다중삭제</a>"
                                document.getElementById("txtPanelAddNotGroupSet").innerHTML += txt;
                            }
                    }

                  }
              })
            }
        function getTxtGroup(){
            $.ajax({
                  type: "GET",
                  url: "/getTxtGroup",
                  data: {},
                  success: function (response) {
                      let dbG = response['dbG']
                      document.getElementById("txtPanelAddGroup").innerHTML = "";
                      for (let i = 0; i < dbG.length; i++){
                            var txt = "<br><label><input type = 'txt' name = 'reGroup' autocomplete='off' value = '" + dbG[i]['조 이름'] + "'></label>";
                            document.getElementById("txtPanelAddGroup").innerHTML += txt;
                            if(i==dbG.length-1){
                                var txt = " <label><a href='#' class= 'myButtonCGroup' onclick='insertGroupTxt()'>+</a></label>";
                                document.getElementById("txtPanelAddGroup").innerHTML += txt;
                            }
                            }

                      }
              })
            }

        function insertGroupTxt(){
            var txt = "<br><label><input type = 'txt' name = 'reGroup' value ='그룹추가(공백불가능)' autocomplete='off'></label>";
            document.getElementById("txtPanelAddGroup").innerHTML += txt;
            var txt = " <label><a href='#' class= 'myButtonCGroup' onclick='insertGroupTxt()'>+</a></label>";
            document.getElementById("txtPanelAddGroup").innerHTML += txt;
        }
        var getGroupList = []

        function getGroup(){
            $.ajax({
                  type: "GET",
                  url: "/getGroup",
                  data: {},
                  success: function (response) {
                      createCheckBox()
                      getTxtGroup()
                      getGroupList = response['dbG']
                      let dbG = response['dbG']
                      for(let n = 0; n<getGroupList.length; n++){
                          $("#textGroup").append('<option value="' + getGroupList[n]['조 이름'] + '">' + getGroupList[n]['조 이름'] + '</option>')
                          $("#textAddPeopleGroup").append('<option value="' + getGroupList[n]['조 이름'] + '">' + getGroupList[n]['조 이름'] + '</option>')
                      }
                  }
              })
           }
        function setGroup(){
            var lenNameGroup = $('input[name=reGroup]').length;
                            var strGroup = String();
                            for(let i = 0; i < lenNameGroup; i++){
                                var valueName = $('input[name = reGroup]').eq(i).val();
                                strGroup += valueName + " ";
                            }
            if(confirm(strGroup + "그룹을 저장하시겠습니까?") == true){
                $.ajax({
                        type: "POST",
                        url: "/setGroup",
                        data: {strGroup : strGroup},
                        success: function (response) {
                            if(response['False'] == 'False'){
                                alert("로그인이 필요한 서비스입니다.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['one'] == 'one'){
                                if(confirm("기존 그룹명 "+response['b']+ "의 인원들을\n"+response['a']+ "그룹으로 변경하시겠습니까?\n※ "+response['b']+" => "+response['a']) == true){
                                    $.ajax({
                                        type: "POST",
                                        url: "/setGroupOne",
                                        data: {b : response['b'], a : response['a']},
                                        success: function (response) {
                                               alert(response['msg']);
                                               window.location.reload();
                                            }

                                    })
                                }
                                else{
                                    alert('인원들의 그룹변경없이 창을 새로고침합니다!');
                                    window.location.reload();
                                }
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
               })
            }
        }
       function clearTextBox(){
                document.getElementById("txtPanelAddCheckbox").innerHTML = "";
       }
       function changeGroup(){
                getCheckboxValue();
                if((document.getElementById('result').innerText == "")){
                    alert("해당 인원을 확인하세요");
                    document.getElementById('result').innerText = ""
                    result = ""
                }
                else{
                var s = $("#textGroup option:selected").val();
                console.log(s);
                if(confirm(document.getElementById('result').innerText + "\n해당 인원의 조를 "+s+"로 변경하시겠습니까?") == true){
                    let nameChangeGroup = document.getElementById('result').innerText;
                    let selectedGroup = $("#textGroup option:selected").val();
                    $.ajax({
                            type: "POST",
                            url: "/changeGroupU",
                            data: {peopleList:nameChangeGroup, new_give:selectedGroup},
                            success: function (response) {
                                if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                                else if(response['False'] == 'Auth'){
                                    alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                                else{
                                    alert("조 변경 완료!");
                                    window.location.reload();
                                }
                            }
                           })
                }else{
                    document.getElementById('result').innerText = ""
                    result = ""
                }
            }
        }
        function insertPeopleDB(){
            if((confirm("이름 : " +$('#textManagePeople').val() + "\n나이 : " +$('#textManagePeopleAge').val() + "\n조 : " + $("#textAddPeopleGroup option:selected").val()+"\n성별 : " +$("input[type=radio][name=sSelect]:checked").val() +"\n특이사항 : " + $('#textManagePeopleInfo').val() + "\n인원을 저장하시겠습니까?")) == true){

                var value_n = $('#textManagePeople').val();
                var value_a = $('#textManagePeopleAge').val();
                var value = $("input[type=radio][name=sSelect]:checked").val()
                if ((value) && (value_n != "") && (value_a != "")) {
                    let name = $('#textManagePeople').val();
                    let age = $('#textManagePeopleAge').val();
                    let group = $("#textAddPeopleGroup option:selected").val();
                    let sSelect = $("input[type=radio][name=sSelect]:checked").val();
                    let info = $('#textManagePeopleInfo').val();
                    $.ajax({
                        type: "POST",
                        url: "/dbPersonAdd",
                        data: {name:name, age:age, group:group, sSelect:sSelect, info:info},
                        success: function (response) {
                            if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['no'] == '같은 이름의 사람이 있습니다!'){
                                alert("이름이 같은 사람이 존재합니다!\n추가하실때 이름 뒤에 알파벳을 추가해주세요. \n예) "+name+" 이/가 존재할 경우 "+name+"B");
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                   })
                }
                else {
                    alert('이름, 나이, 성별, 그룹을 확인해주세요!');
                }
           }
        }
        function replacePeopleDB(){
            if((confirm("이름 : " +$('#textManagePeople').val()  + "\n나이 : " +$('#textManagePeopleAge').val() + "\n조 : " + $("#textAddPeopleGroup option:selected").val()+"\n성별 : " +$("input[type=radio][name=sSelect]:checked").val() +"\n특이사항 : "+ $('#textManagePeopleInfo').val()+"\n인원정보를 변경하시겠습니까?")) == true){
                var value_n = $('#textManagePeople').val();
                var value_a = $('#textManagePeopleAge').val();
                var value = $("input[type=radio][name=sSelect]:checked").val()
                if ((value) && (value_n != "") && (value_a != "")) {
                    let name = $('#textManagePeople').val();
                    let age = $('#textManagePeopleAge').val();
                    let group = $("#textAddPeopleGroup option:selected").val();
                    let sSelect = $("input[type=radio][name=sSelect]:checked").val();
                    let info = $('#textManagePeopleInfo').val();
                    $.ajax({
                        type: "POST",
                        url: "/dbPersonChange",
                        data: {name:name, age:age, group:group, sSelect:sSelect, info:info},
                        success: function (response) {
                            if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['no'] == '같은 이름의 사람이 없습니다!'){
                                alert("이름이 같은 사람이 존재하지않습니다!\n변경하실 사람의 이름을 확인해주세요");
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                   })
                }

                else {
                    alert('이름, 성별, 그룹을 확인해주세요!');
                }
           }
        }
        function autoSave(){
            if(confirm("메일백업?") == true){
               $.ajax({
                type: "GET",
                url: "/autoSave",
                data: {},
                success: function (response) {
                    if(response['False'] == 'False'){
                        alert("로그인이 필요한 서비스입니다.");
                        document.getElementById('result').innerText = ""
                        result = ""
                    }
                    else if(response['False'] == 'Auth'){
                        alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                        document.getElementById('result').innerText = ""
                        result = ""
                    }
                    else{
                        alert(response['msg']);
                        window.location.reload();
                    }
                }
               })
            }
        }
        function delMultiPeopleDB(){
            getCheckboxValue()
            if((document.getElementById('result').innerText == "")){
                        alert("해당 인원을 확인하세요");
                        document.getElementById('result').innerText = ""
                        result = ""
                    }
            else{
                if(confirm(result + "\n인원을 삭제하시겠습니까?") == true){
                    let name = document.getElementById('result').innerText;
                    $.ajax({
                            type: "POST",
                            url: "/delMultiPeople",
                            data: {name:name},
                            success: function (response) {
                                if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                                else if(response['False'] == 'Auth'){
                                    alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                                else{
                                    alert(response['msg']);
                                    window.location.reload();
                                }
                            }
                           })
                }
                else{
                    document.getElementById('result').innerText = ""
                    result = ""

                }
            }
        }
        function deletePeopleDB(){
            if((confirm("이름 : " +$('#textManagePeople').val() + "\n조 : " + $("#textAddPeopleGroup option:selected").val()+"\n인원을 삭제하시겠습니까?")) == true){
                if($('#textManagePeople').val() =='' || $("#textAddPeopleGroup option:selected").val() ==''){
                    alert("이름 및 조를 확인해주세요!");
                }
                else{
                    let name = $('#textManagePeople').val();
                    let group = $("#textAddPeopleGroup option:selected").val();

                    $.ajax({
                        type: "POST",
                        url: "/dbPersonDel",
                        data: {name:name, group:group},
                        success: function (response) {
                            if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else if(response['no'] == 'DB에 저장된 인원이 없습니다!'){
                                alert("DB에 저장된 인원이 없습니다! 확인해주세요.");
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                   })
                }
            }
        }
        function whoIs(element){
            if(element.이름 === String(etv)){
                return true;
            }
        }

        function getCheckboxInfo(event)  {
            etv = event.target.value;
            document.getElementById('textManagePeople').value = event.target.value;
            $("#textAddPeopleGroup").val(event.target.name).trigger('change');
            console.log(dbP);
            const peoInfo = dbP.find(whoIs);
            console.log(peoInfo);
            if (peoInfo.성별[0] == '남'){
                $("input:radio[name='sSelect']:radio[value='남']").prop('checked', true);
            }
            else{
                $("input:radio[name='sSelect']:radio[value='여']").prop('checked', true);
            }
            document.getElementById('textManagePeopleInfo').value = peoInfo.특이사항[0];
            document.getElementById('textManagePeopleAge').value = peoInfo.나이[0];
        }
        function getNSGCheckboxInfo(event)  {
            etv = event.target.value;
            document.getElementById('textManagePeople').value = event.target.value;
            $("#textAddPeopleGroup").val(event.target.name).trigger('change');
            console.log(dbNSP);
            const peoInfo = dbNSP.find(whoIs);
            console.log(peoInfo);
            if (peoInfo.성별[0] == '남'){
                $("input:radio[name='sSelect']:radio[value='남']").prop('checked', true);
            }
            else{
                $("input:radio[name='sSelect']:radio[value='여']").prop('checked', true);
            }
            document.getElementById('textManagePeopleInfo').value = peoInfo.특이사항[0];
            document.getElementById('textManagePeopleAge').value = peoInfo.나이[0];
        }
        function displayPeopleInfo(){
            var v = $("input[type=radio][name=infoSelect]:checked").val()
            console.log(v);
            if(v == '0'){
                console.log("보기");
                document.getElementById("resultCheckbox").style.display = 'flex';
                console.log(document.getElementById("resultCheckbox").style.display);
            }
            else{
                console.log("숨김");
                document.getElementById("resultCheckbox").style.display = 'none';
                console.log(document.getElementById("resultCheckbox").style.display);
            }
        }
        function checkboxDateS(){
            var test1 = document.getElementById('checkboxDateC');
            if($(test1).is(":checked") == true){
                $("#title").attr("disabled", false);
            }
            else{
                $("#title").attr("disabled", true);
            }

        }

        function ageAdd(){
            if((confirm("전체인원의 나이를 증가시키겠습니까?")) == true){
                $.ajax({
                        type: "POST",
                        url: "/ageAdd",
                        success: function (response) {
                            if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                   })
            }
        }
        function ageDown(){
            if((confirm("전체인원의 나이를 감소시키겠습니까?")) == true){
                $.ajax({
                        type: "POST",
                        url: "/ageDown",
                        success: function (response) {
                            if(response['False'] == 'False'){
                                    alert("로그인이 필요한 서비스입니다.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                            else if(response['False'] == 'Auth'){
                                alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                document.getElementById('result').innerText = ""
                                result = ""
                            }
                            else{
                                alert(response["msg"]);
                                window.location.reload();
                            }
                        }
                   })
            }
        }
        function mailBackup(){
            var mail = prompt("※이 기능은 출석체크를 진행한 후 저장된 내용을 메일로 보내주는 기능입니다.\n메일을 전달받을 이메일주소와 본인의 이름을 옆의 형식에 맞게 아래에 적어주세요\n메일주소@도메인/이름","naochugu@gmail.com/김상현");
            console.log(mail);
                if(mail != ""){
                    $.ajax({
                            type: "POST",
                            url: "/mailBackup",
                            data: {mail:mail},
                            success: function (response) {
                                if(response['False'] == 'False'){
                                        alert("로그인이 필요한 서비스입니다.");
                                        document.getElementById('result').innerText = ""
                                        result = ""
                                }
                                else if(response['False'] == 'Auth'){
                                    alert("로그인된 계정의 권한이 없습니다.\nadmin권한의 계정을 사용해주세요.");
                                    document.getElementById('result').innerText = ""
                                    result = ""
                                }
                                else if(response['success']){
                                    alert(response["success"]);
                                    window.location.reload();
                                }
                                else{
                                    alert(response["msg"]);
                                }
                            }
                    })
                }
        }