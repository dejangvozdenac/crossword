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
      elem.id = localStorage.getItem("h_" + x + "_" + y) + "." + localStorage.getItem("v_" + x + "_" + y) + "." + parseInt(i / width) + "." + i % width + "." + localStorage.getItem("a_" + x + "_" + y);
    } else {
      elem.id = "-1.-1" + parseInt(i / width) + "." + i % width;
    }
    index++;
  }
}

function storeClueIndex() {
  {% for row in range(0, state.height) %}
    {% for col in range(0, state.width) %}
      {% if state.grid[row][col].color != "." %}
        localStorage.setItem("a_" + {{ row }} + "_" + {{ col }} , {{ state._get_answer(row, col) }});

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
  firstCell = true;

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
        if (firstCell) {
          markCell(tags[2], tags[3]);
          firstCell = false;
        }
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

function clueAtIndex(direction, index) {
  if (direction == "Across") {
    clues = document.getElementById('across_hidden').getElementsByTagName("div");
  } else {
    clues = document.getElementById('down_hidden').getElementsByTagName("div");
  }

  if(index >= clues.length || index < 0) {
    return " ";
  }

  return clues[index].innerHTML;
}

function lastIndex(direction) {
  if (direction == "Across") {
    return document.getElementById('across_hidden').getElementsByTagName("div").length - 1;
  } else {
    return document.getElementById('down_hidden').getElementsByTagName("div").length - 1;
  }
}

function initCurrentClue() {
  {% if state.current_clue_direction == "Across" %}
    setCurrentClue("Across", {{ state.current_clue_index }});
  {% else %}
    setCurrentClue("Down", {{ state.current_clue_index }});  
  {% endif %}
}

function colorCell(row, col, color) {
  div = document.getElementById("wrapper");
  subDiv = div.getElementsByTagName("div");

  for(var i = 0; i < subDiv.length; i++) {
      var elem = subDiv[i];
      tags = elem.id.split(".");
      cell_x = tags[2];
      cell_y = tags[3];

      if (cell_x == row && cell_y == col) {
        $(elem).css("background", color);
      }
  }
}

function markCell(row, col) {
  localStorage.setItem("selectedCell",  row + "_" + col);
  colorCell(row, col, "DarkGray");
}


function unmarkCell() {
  selectedCell = localStorage.getItem("selectedCell");
  row = parseInt(selectedCell.split("_")[0]);
  col = parseInt(selectedCell.split("_")[1]);

  colorCell(row, col, "LightGray");
}

function fillCell(row, col, key) {
  div = document.getElementById("wrapper");
  subDiv = div.getElementsByTagName("div");

  for(var i = 0; i < subDiv.length; i++) {
    var elem = subDiv[i];
    tags = elem.id.split(".");
    cell_x = tags[2];
    cell_y = tags[3];

    if (cell_x == row && cell_y == col) {
      if (key == 32 || key == 8) {
        elem.innerHTML = '';
      } else {
        elem.innerHTML = '<div class="letter" style="background: none 0% 0% / auto repeat scroll padding-box border-box rgba(0, 0, 0, 0);">' + String.fromCharCode((96 <= key && key <= 105)? key-48 : key) + '</div>';
      }
    }
  }
}

function checkGrid() {
  div = document.getElementById("wrapper");
  subDiv = div.getElementsByTagName("div");

  for(var i = 0; i < subDiv.length; i++) {
    var elem = subDiv[i];
    tags = elem.id.split(".");
    cell_x = tags[2];
    cell_y = tags[3];

    if(tags[0] == -1) {
      continue;
    }

    answer = tags[4];
    letterDiv = elem.getElementsByTagName("div");

    if (letterDiv.length == 0) {
      continue;
    }

    console.log(answer)

    content = letterDiv[0].innerHTML;
    console.log(content);
    console.log(String.fromCharCode(answer))
    if (content != String.fromCharCode(answer)) {
      $(letterDiv[0]).css("color", "red");
    }
  }
}




function setCurrentClue(clueDirection, nextIndex) {
  var nextClue = clueAtIndex(clueDirection, nextIndex);

  if (nextClue == " ") {
    clueDirection = (clueDirection == "Across") ? "Down" : "Across";
    if (nextIndex != -1) {
      nextIndex = 0;
    } else {
      nextIndex = lastIndex(clueDirection);
    }
    nextClue = clueAtIndex(clueDirection, nextIndex);
  }

  var nextNumber = nextClue.split(".")[0];

  markSelectedClue(clueDirection, nextIndex);

  $("#clueText").val(nextNumber + " " + clueDirection[0]);
  $("#clueText").css("color", "red");
  // $("#solutionText").focus();

  document.getElementById("selected_clue").innerHTML = nextNumber + " " + clueDirection + ":" + nextClue.substr(nextNumber.length + 1);
}

$(document).click(function(event) {      
  var clueObj = event.target;

  if ($(clueObj)["0"].className != "empty" && $(clueObj)["0"].className != "empty numbered" &&
    $(clueObj)["0"].className != "letter" && 
    clueObj.parentNode.className != "col" && clueObj.parentNode.className != "colright") 
  {
    return
  } else if ($(clueObj).text() == "Across" || $(clueObj).text() == "Down") {
    return
  }

  if ($(clueObj)["0"].className == "empty" || $(clueObj)["0"].className == "empty numbered" || $(clueObj)["0"].className == "letter" || $(clueObj)["0"].className == "circle") {
    
    if (event.shiftKey) {
      if ($(clueObj)["0"].className == "letter"){
        clueObj = clueObj.parentNode;
      }
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
      acrossObj = document.getElementById('across_hidden').getElementsByTagName("div")[x_order]
      clueObj = acrossObj
    }

    if (x_order != -1 && y_order != -1){
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
  // $("#solutionText").focus();
  document.getElementById("selected_clue").innerHTML = clueNumber + " " + direction + ":" + text.substr(clueNumber.length + 1);
});

function GetCurrentDirection() {
  var currentClue = document.getElementById("selected_clue").innerHTML;
  var clueNumberAndDirection = currentClue.split(":")[0];
  var clueNumber = clueNumberAndDirection.split(" ")[0];
  return clueNumberAndDirection.split(" ")[1];
}

function isValid(row, col) {
  if (row < 0 || col < 0 || row >= {{ state.height }} || col >= {{ state.width }} ) {
    return false;
  }

  for(var i = 0; i < subDiv.length; i++) {
    var elem = subDiv[i];
    tags = elem.id.split(".");
    cell_x = tags[2];
    cell_y = tags[3];

    if (cell_x == row && cell_y == col) {
      if (tags[0] == - 1 || tags[1] == - 1) {
        return false;
      } else {
        return true;
      }
    }
  }

}

function TabEvent(evt) {
  evt.preventDefault();
  var increment = evt.shiftKey ? -1 : 1;

  var currentClue = document.getElementById("selected_clue").innerHTML;
  if (currentClue == "") {
    var nextIndex = 0;
    var clueDirection =  "Across";
  } else {
    var clueNumberAndDirection = currentClue.split(":")[0];
    var clueNumber = clueNumberAndDirection.split(" ")[0];
    var clueDirection = clueNumberAndDirection.split(" ")[1];
    var clueText = currentClue.substr(clueNumberAndDirection.length + 1);
    clueText = clueText.substr(1, clueText.length);
    var nextIndex = findClueIndex(clueDirection, clueNumber + ". " + clueText) + increment;
  }

  setCurrentClue(clueDirection, nextIndex);
}

function ArrowEvent(keyCode) {
  selectedCell = localStorage.getItem("selectedCell");
  x = parseInt(selectedCell.split("_")[0]);
  y = parseInt(selectedCell.split("_")[1]);
  if (keyCode == 40) {
    x_offset = 1;
    y_offset = 0;
  } else if (keyCode == 38) {
    x_offset = - 1;
    y_offset = 0;
  } else if (keyCode == 39) {
    x_offset = 0;
    y_offset = 1;
  } else if (keyCode == 37) {
    x_offset = 0;
    y_offset = - 1;
  }
  if (isValid(x + x_offset, y + y_offset)) {
    unmarkCell();
    markCell(x + x_offset, y + y_offset);
  }
}

function KeyPress(evt) {
  var evt = (evt) ? evt : ((event) ? event : null);
  if(evt.keyCode == 9) {
    TabEvent(evt);
  } else if (evt.keyCode == 37 || evt.keyCode == 38 || evt.keyCode == 39 || evt.keyCode == 40) {
    ArrowEvent(evt.keyCode);
  } else if ((evt.keyCode >= 65 && evt.keyCode <= 90) || evt.keyCode == 32 || evt.keyCode == 8) {
    selectedCell = localStorage.getItem("selectedCell");
    x = parseInt(selectedCell.split("_")[0]);
    y = parseInt(selectedCell.split("_")[1]);

    fillCell(x, y, evt.keyCode);
    currendDirection = GetCurrentDirection();
    if (currendDirection == "Across") {
      if (evt.keyCode == 8){
        ArrowEvent(37)
      } else {
        ArrowEvent(39);
      }
    } else {
      if (evt.keyCode == 8){
        ArrowEvent(38)
      } else {
        ArrowEvent(40);
      }
    }
  } else if (evt.keyCode == 13) {
    checkGrid();
  }
}

setSize();
storeClueIndex();
tagCellsInGrid();
initCurrentClue();
document.onkeydown = KeyPress;