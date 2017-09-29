function tagCellsInGrid() {
  width = {{ state.width }};
  div = document.getElementById("wrapper");
  subDiv = div.getElementsByTagName("div");
  index = 0;

  for(var i = 0; i < subDiv.length; i++) {
    var elem = subDiv[i];
    if ($(elem)["0"].className != "empty" && $(elem)["0"].className != "empty numbered" && 
      $(elem)["0"].className != "filled") {
      continue;
    }
    x = Math.floor(index / width);
    y = index % width;
    if ($(elem)["0"].className != "filled"){
      elem.id = localStorage.getItem("h_" + x + "_" + y) + "." + localStorage.getItem("v_" + x + "_" + y);
    } else {
      elem.id = "-1.-1";
    }
    index++;
  }
}

function storeClueIndex() {
  {% for row in range(0, state.width) %}
    {% for col in range(0, state.height) %}
      {% if state.grid[row][col].color != "." %}
        {% if state._get_clue_index(row, col, False) != None %}
          localStorage.setItem("v_" + {{ row }} + "_" + {{ col }} , {{ state._get_clue_index(row, col, False) }} );
        {% else %}
          localStorage.setItem("v_" + {{ row }} + "_" + {{ col }} , {{ -1 }} );
        {% endif %}
        {% if state._get_clue_index(row, col, True) != None %}
          localStorage.setItem("h_" + {{ row }} + "_" + {{ col }} , {{ state._get_clue_index(row, col, True) }} );
        {% else %}
          localStorage.setItem("h_" + {{ row }} + "_" + {{ col }} , {{ -1 }} );
        {% endif %}
      {% endif %}
    {% endfor %}
  {% endfor %}
}

function setSize() {
  document.getElementById('wrapper').style.height = 30 * {{ state.height }} + "px";
  document.getElementById('wrapper').style.width = 30 * {{ state.width }} + "px";
}

function markSelectedClue(direction, selectedClueIndex) {
  div = document.getElementById("wrapper");
  subDiv = div.getElementsByTagName("div");

  for(var i = 0; i < subDiv.length; i++) {
      var elem = subDiv[i];
      tags = elem.id.split(".");
      if (direction == "Across") {
        targetIndex = tags[0];
      } else {
        targetIndex = tags[1];
      }

      if (targetIndex == selectedClueIndex && ($(elem)["0"].className == "empty" || $(elem)["0"].className == "empty numbered")) {
        $(elem).css("background", "LightGray");
      } else if ($(elem)["0"].className != "filled"){
        $(elem).css("background", "rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box");
      }
  }
}

function findClueIndex(direction, text) {
  if (direction == "Across") {
    clues = document.getElementById('across_hidden').getElementsByTagName("div");
  } else {
    clues = document.getElementById('down_hidden').getElementsByTagName("div");
  }

  for(var i = 0; i < clues.length; i++) {
    var clue = clues[i];
    if (text == $(clue).text()) {
      return i;
    }
  }
  return -1;
}

$(document).click(function(event) {      
  var clueObj = event.target;

  if ($(clueObj)["0"].className == "empty" || $(clueObj)["0"].className == "empty numbered" || $(clueObj)["0"].className == "letter" || $(clueObj)["0"].className == "circle") {
    
    if (event.shiftKey) {
      if ($(clueObj)["0"].className == "letter"){
        clueObj = clueObj.parentNode;
      }
      console.log($(clueObj).css("background") == "rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box");
      if ($(clueObj).css("background") == "rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box") {
        $(clueObj).css("background", "LightGray");
      } else {
        $(clueObj).css("background", "rgba(0, 0, 0, 0) none repeat scroll 0% 0% / auto padding-box border-box");
      }
      return;
    }

    y = Math.floor((event.pageX - document.getElementById('wrapper').getBoundingClientRect().left + 1) / 30)
    x = Math.floor((event.pageY - document.getElementById('wrapper').getBoundingClientRect().top + 1) / 30)
    x_order = localStorage.getItem("h_" + x + "_" + y)
    y_order = localStorage.getItem("v_" + x + "_" + y)
    
    if (x_order != -1) {
      acrossObj = document.getElementById('across_hidden').getElementsByTagName("div")[x_order]
    } else {
      downObj   = document.getElementById('down_hidden').getElementsByTagName("div")[y_order]
      clueObj = downObj
    }

    if (y_order != -1) {
      downObj   = document.getElementById('down_hidden').getElementsByTagName("div")[y_order]
    } else {
      console.log(x_order)
      acrossObj = document.getElementById('across_hidden').getElementsByTagName("div")[x_order]
      clueObj = acrossObj
    }

    if (x_order != -1 && y != -1){
      if($("#clueText").val() == $(acrossObj).text().split(".")[0] + " " + acrossObj.parentNode.getElementsByTagName("h2")[0].innerHTML[0]) {
        clueObj = downObj
      } else {
        clueObj = acrossObj
      }
    }
  } 
  var text = $(clueObj).text();
  var clueNumber = text.split(".")[0];
  var direction = clueObj.parentNode.getElementsByTagName("h2")[0].innerHTML;

  markSelectedClue(direction, findClueIndex(direction, text));

  $("#clueText").val(clueNumber + " " + direction[0]);
  $("#clueText").css("color", "red");
  $("#solutionText").focus();
  document.getElementById("selected_clue").innerHTML = clueNumber + " " + direction + ":" + text.substr(clueNumber.length + 1);
});

setSize();
storeClueIndex();
tagCellsInGrid();