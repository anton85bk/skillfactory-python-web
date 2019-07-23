const numDivs = 36;
const maxHits = 10;

let hits = 0;
let firstHitTime = 0;
let missed = 0;

function round() {
  $(".target").removeClass("target");
  let divSelector = randomDivId();
  $(divSelector).addClass("target");
  $(".target").text(hits + 1);

  if (hits == 0) {
    firstHitTime = getTimestamp();
  }

  if (hits === maxHits) {
    endGame();
  }
}

function endGame() {
  console.log("endGame()")
  // hide gamefield:
  $(".game-field").addClass("d-none");
  // calculate result:
  let totalPlayedMillis = getTimestamp() - firstHitTime;
  let totalPlayedSeconds = Number(totalPlayedMillis / 1000).toPrecision(3);
  // display result:
  $("#total-time-played").text(totalPlayedSeconds);
  $("#win-message").removeClass("d-none");
  if (missed) {
    $("#total-missed-message-counter").text(missed);
    $(".total-missed-message").removeClass("d-none");
  }
  $("#total-score").text(maxHits - missed);
}

function handleClick(event) {
  if (firstHitTime != 0) {
    // if game started:
    if ($(event.target).hasClass("target")) {
      // if we hit the target:
      $(".miss").removeClass("miss");
      $(".target").text("");
      hits = hits + 1;
      round();

    } else {
      // if we missed:
      $(event.target).addClass("miss")
      missed += 1;
    }
  }
}

function init() {
  $(".game-field").click(handleClick);

  $("#button-start").click(function() {
    round();
    $("#button-start").addClass("d-none");
    $("#button-reload").removeClass("d-none");
  });
  $("#button-reload").click(function() {
    location.reload();
  });
}

$(document).ready(init);
