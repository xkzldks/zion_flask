
    chul = '';
    date = new Date().toLocaleDateString();
    //다운로드 하이퍼링크에 클릭 이벤트 발생시 saveCSV 함수를 호출하도록 이벤트 리스너를 추가
    document.addEventListener('DOMContentLoaded', function(){
      document.getElementById('download').addEventListener('click', function(){
        saveCSV('data.csv'); // CSV파일 다운로드 함수 호출
        return false;
      })
    });

    //CSV 생성 함수
    function saveCSV(fileName){
        //CSV 문자열 생성
        let downLink = document.getElementById('download');
        const BOM = "\uFEFF";
        let csv = ''; //CSV최종 문자열을 저장하는 변수
        csv = BOM +csv
        let rows = document.querySelectorAll("#csvtable tr"); // 테이블에서 행 요소들을 모두 선택

        //행단위 루핑
        for (var i = 0; i < rows.length; i++) {
            let cells = rows[i].querySelectorAll("td, th");
            let row = [];
            //행의 셀 값을 배열로 얻기
            cells.forEach(function(cell){
              row.push(cell.innerHTML);
            });

            csv += row.join(',') + (i != rows.length-1 ? '\n':''); // 배열을 문자열+줄바꿈으로 변환
        }

        //CSV 파일 저장
        csvFile = new Blob([csv], {type: "text/csv"}); // 생성한 CSV 문자열을 Blob 데이터로 생성
        downLink.href = window.URL.createObjectURL(csvFile); // Blob 데이터를 URL 객체로 감싸 다운로드 하이퍼링크에 붙임.
        downLink.download = fileName; // 인자로 받은 다운로드 파일명을 지정
    }
    $(function(){
          $(".fold-table tr.view").on("click", function(){
            if($(this).hasClass("open")) {
              $(this).removeClass("open").next(".fold").removeClass("open");
            } else {
              $(".fold-table tr.view").removeClass("open").next(".fold").removeClass("open");
              $(this).addClass("open").next(".fold").addClass("open");
            }
          });
        });
        $(document).ready(function () {
//            google.load('visualization', '1', {packages: ['corechart']});
            dateLoad();
            google.charts.load('current',{'packages':['corechart']});
            google.charts.load('current', {'packages':['bar']});
            google.charts.load('current', {'packages':['line']});
            getAttendanceGraph();
            getTDate();
            getTChul();


        });
        function dateLoad(){
            $.ajax({
                type: "GET",
                url: "/dateLoad",
                data: {},
                success: function (response) {
                    let startDay = response['startDay'];
                    let endDay = response['endDay'];
                    document.getElementById('from').value= startDay;
                    document.getElementById('to').value= endDay;
                }
            })
        }

        function getTChul(){
            $.ajax({
                    type: "GET",
                    url: "/getTChul",
                    data: {},
                    success: function (response) {
                        chul = response['chul']
                        console.log(chul);
                        console.log(chul.length);
                           for( let i = 0; i < chul.length; i++){
                               txt = ''
                               for(let k = 0; k <chul[i].length; k++){
                                    if(k == 0){
                                        txt += "<tr><td class = 'tdz' style = 'color : #fff;background: #42444e; position: sticky; z-index: 0; left: 0px;'>"+chul[i][k]+"</td>"
                                    }
                                    else if(k == chul[i].length){
                                        txt += "<td class = 'tdz'>"+chul[i][k]+"</td><tr>"
                                    }
                                    else{
                                        txt += "<td class = 'tdz'>"+chul[i][k]+"</td>"
                                    }

                               }document.getElementById("tChul").innerHTML += txt;

                           }

                    }
                })
        }
        function getTDate(){
            $.ajax({
                    type: "GET",
                    url: "/getTDate",
                    data: {},
                    success: function (response) {
                        let date = response['date']
                        if (date.length != 0){
                            for (let i = 0; i < date.length; i++){
                                 var txt = "<th class = 'thz' style = 'z-index: 1;'>"+date[i]+"</th>"
                                 document.getElementById("tDate").innerHTML += txt;
                            }

                        }
                        else{
                            var txt = "<h3>데이터가 부족합니다</h3>"
                            document.getElementById("tDate").innerHTML += txt;
                        }
                    }
                })
        }
        function weekCount(today) {
          var year = dt.getFullYear();
          var countDay = new Date(year,0,1);
          var week = 1;
          while(today>countDay){
            countDay.setDate(countDay.getDate()+ 1);
            var countNum = countDay.getDay();
            if(countNum == 0){
              week++;
            }
          }
          return week;
        }
        var dt = new Date();
//        console.log(weekCount(dt));
        var dateTxt = weekCount(dt);
//        console.log(dateTxt);
<!--        document.getElementById("datePanel").innerHTML += dateTxt;-->

        function getAttendanceGraph() {
            document.getElementById("graphPanel").innerHTML = "";
                       $.ajax({
                            type: "GET",
                            url: "/getAttendanceGraph",
                            data: {},
                            success: function (response) {
                                let chul = response['chul'];
                                for (let i = 0; i < chul.length; i++){
                                    if (chul.length != 0){
                                        if ((chul[i][1]/48*100).toFixed(1)> 70){
                                            console.log(chul[i][0] + (chul[i][1]/48*100).toFixed(1));
                                            var txt = "<div class='zt-skill-bar'><div data-width='"+chul[i][1]+"' style = 'white-space : nowrap; width:"+(chul[i][1]/48*100)+"%;'>"+(i+1)+". "+chul[i][0]+" | "+chul[i][1]+"일 | "+(chul[i][1]/48*100).toFixed(1)+"%</div></div>"
                                            document.getElementById("graphPanel").innerHTML += txt;
                                        }
                                        else{
                                            var txt = "<div class='xt-skill-bar'><div data-width='"+chul[i][1]+"' style = 'white-space : nowrap; width:"+(chul[i][1]/48*100)+"%;'>"+(i+1)+". "+chul[i][0]+" | "+chul[i][1]+"일 | "+(chul[i][1]/48*100).toFixed(1)+"%</div></div>"
                                            document.getElementById("graphPanel").innerHTML += txt;
                                        }
                                    }
                                    else{
                                        var txt = "<h3>데이터가 부족합니다</h3>"
                                        document.getElementById("graphPanel").innerHTML += txt;
                                    }
                                }
                            }
                        })
                    }
        function getGroupGraph() {
            document.getElementById("graphPanel").innerHTML = "";
                    $.ajax({
                            type: "GET",
                            url: "/getGroupGraph",
                            data: {},
                            success: function (response) {
                                if(response['error'] != 'error'){
                                    let chul = response['chul']
                                    console.log(chul);
    <!--                                    txt = chul;-->
    <!--                                    document.getElementById("graphPanel").innerHTML += txt;-->
                                    document.getElementById('graphPanel').style.width = '100%';
                                    document.getElementById('graphPanel').style.height = '500%';
                                    var data = google.visualization.arrayToDataTable(chul);
                                    console.log(data);
                                    var options = {
                                        chartType   : 'Line Chart',
                                        title : '월별 조 출석현황',
                                        vAxis: {title: "인원 수"},
                                        hAxis: {title: "월"},
                                        seriesType: "bars",
                                        height:500,
                                        width:"150%",
                                        legend:{position:"top"},
                                        isStacked:false,
                                        animation:{
                                            startup: true,
                                            duration: 1000,
                                            easing: 'linear'
                                        },
                                        series: {5: {type: "line"}},
                                        annotations:{
                                            textStyle:{
                                            fontSize: 5,
                                            bold: false,
                                            opacity: 1.8
                                            }
                                            }
                                        };
                                    var chart = new google.charts.Bar(document.getElementById('graphPanel'));
                                    chart.draw(data, google.charts.Bar.convertOptions(options));
                                }
                                else if(response['error'] == 'error'){
                                    document.getElementById("graphPanel").innerHTML = "미분류 그룹에 인원이 있습니다. 해당하는 조에 배치하거나 인원을 삭제해 주시기바랍니다.";
                                }
                            }
                        })

            }

        function getGroupGraph2() {
            document.getElementById("graphPanel").innerHTML = "";
                    $.ajax({
                            type: "GET",
                            url: "/getGroupGraph2",
                            data: {},
                            success: function (response) {
                                if(response['error'] != 'error'){
                                    let chul = response['chul']
                                    console.log(chul);
    <!--                                    txt = chul;-->
    <!--                                    document.getElementById("graphPanel").innerHTML += txt;-->
                                    document.getElementById('graphPanel').style.width = '100%';
                                    document.getElementById('graphPanel').style.height = '500%';
                                    var data = google.visualization.arrayToDataTable(chul);
                                    console.log(data);
                                    var options = {
                                        title : '월별 조 출석평균',
                                        vAxis: {title: "%(퍼센트)"},
                                        hAxis: {title: "월"},
                                        seriesType: "bars",
                                        height:500,
                                        width:"150%",
                                        series: {5: {type: "line"}}
                                        };
                                    var chart = new google.charts.Bar(document.getElementById('graphPanel'));
                                    chart.draw(data, google.charts.Bar.convertOptions(options));
                                }
                                else if(response['error'] == 'error'){
                                        document.getElementById("graphPanel").innerHTML = "미분류 그룹에 인원이 있습니다. 해당하는 조에 배치하거나 인원을 삭제해 주시기바랍니다.";
                                }
                            }
                        })

            }
        function getAgeGraph() {
            document.getElementById("graphPanel").innerHTML = "";
                    $.ajax({
                            type: "GET",
                            url: "/getAgeGraph",
                            data: {},
                            success: function (response) {
                                if(response['error'] != 'error'){
                                    let chul = response['chul']
                                    console.log(chul);
    <!--                                    txt = chul;-->
    <!--                                    document.getElementById("graphPanel").innerHTML += txt;-->
                                    document.getElementById('graphPanel').style.width = '100%';
                                    document.getElementById('graphPanel').style.height = '500%';
                                    var data = google.visualization.arrayToDataTable(chul);
                                    console.log(data);
                                    var options = {
                                        title : '월별 나이별 출석평균',
                                        vAxis: {title: "%(퍼센트)"},
                                        hAxis: {title: "월"},
                                        seriesType: "bars",
                                        height:500,
                                        width:"150%",
                                        series: {5: {type: "line"}}
                                        };
                                    var chart = new google.charts.Line(document.getElementById('graphPanel'));
                                    chart.draw(data, google.charts.Line.convertOptions(options));
                                }
                                else if(response['error'] == 'error'){
                                    document.getElementById("graphPanel").innerHTML = "미분류 그룹에 인원이 있습니다. 해당하는 조에 배치하거나 인원을 삭제해 주시기바랍니다.";
                                }
                            }
                   })

            }
        $(window).scroll(function(){
             $(".csvtable").css("left",0-$(this).scrollLeft());
            })



        function dateSave(){
            let from = $( "#from" ).val();
            let to = $( "#to" ).val();
                if(from != '' && to !=''){
                    $.ajax({
                            type: "POST",
                            url: "/dateSave",
                            data: {from : from, to : to},
                            success: function (response) {
                                        alert(response["msg"]);
                                        window.location.reload();

                            }
                    })
                }
                else{
                    alert("시작날짜와 끝날짜를 확인해주세요.");
                }
        }
        $(function(){
            var option =  {
              // datepicker 애니메이션 타입
              // option 종류 : "show" , "slideDown", "fadeIn", "blind", "bounce", "clip", "drop", "fold", "slide"
              showAnim : "show",
              // 해당 월의 다른 월의 날짜가 보이는 여부, 예를 들면 10월이면 전후에 9월 마지막과 11월의 시작 일이 보이는 여부입니다. 즉, 달력이 꽉 차 보이게 하는 것
              showOtherMonths: false,
              // 선택 여부 (showOtherMonths 옵션과 같이 일치시키지 않으면 에러가 발생합니다.)
              selectOtherMonths: false,
              // 달력 밑에 오늘과 닫기 버튼이 보인다.
              showButtonPanel: false,
              // 년 월이 셀렉트 박스로 표현 되어서 선택할 수 있다.
              changeMonth: true,
              changeYear: true,
              nextText : "&nbsp&nbsp&nbsp다음달&nbsp&nbsp&nbsp",
              prevText : "&nbsp&nbsp&nbsp이전달&nbsp&nbsp&nbsp",
              // 한번에 보이는 개월 수
              numberOfMonths: 1,
              // 데이터 포멧
              dateFormat: "yy-mm-dd",
              // 텍스트 박스 옆의 달력 포시
              showOn: "button",
              //이미지 타입인지 버튼 타입인지 설정
              buttonImageOnly: true,
              // 이미지 경로
              buttonImage: "https://jqueryui.com/resources/demos/datepicker/images/calendar.gif",
              // 버튼 타입이면 버튼 값
              buttonText: "Select date",
              // alt 데이터 포멧
              altFormat: "DD, d MM, yy",
        <!--      // 선택 가능한 날짜(수 형식) - 현재 기준 -20일-->
              minDate: "-12M",
              // 선택 가능한 최대 날짜(문자 형식) - 현재 기준 +1월 +20일
              maxDate: "+12M",
              // 주 표시
              showWeek: false
            };
            var optionFrom = option;
            optionFrom.altField = "#alternateFrom";
            var dateFormat = "mm/dd/yy";
            // 시작일이 선택이 되면 종료일은 시작일 보다 앞을 선택할 수 없다.
            var from = $( "#from" )
              .datepicker(optionFrom)
              .on( "change", function() {
                to.datepicker( "option", "minDate", getDate( this ) );
              });

            var optionTo = option;
            optionTo.altField = "#alternateTo";
            // 종료일이 선택이 되면 시작일은 시작일 보다 앞을 선택할 수 없다.
            var to = $( "#to" )
              .datepicker(optionTo)
              .on( "change", function() {
                from.datepicker( "option", "maxDate", getDate( this ) );
              });
            function getDate( element ) {
              return moment(element.value).toDate();
            }
        });