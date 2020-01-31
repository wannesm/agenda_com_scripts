// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-purple; icon-glyph: magic;
// share-sheet-inputs: url, plain-text, file-url;


// Share with Agenda
// Copyright 2019, Wannes Meert


// https://weeknumber.net/how-to/javascript
// This script is released to the public domain and may be used, modified and
// distributed without restrictions. Attribution not necessary but appreciated.
// Source: https://weeknumber.net/how-to/javascript

log("Start script");

// Returns the ISO week of the date.
Date.prototype.getWeek = function() {
  var date = new Date(this.getTime());
  date.setHours(0, 0, 0, 0);
  // Thursday in current week decides the year.
  date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
  // January 4 is always in week 1.
  var week1 = new Date(date.getFullYear(), 0, 4);
  // Adjust to Thursday in week 1 and count number of weeks from date to week1.
  return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                        - 3 + (week1.getDay() + 6) % 7) / 7);
}


var today = new Date()
var week = today.getWeek();
if (week < 10) {
  week = "0" + week;
}
var title = "To Read " + today.getFullYear() + "W" + week;
var project = "To Read";


var input_text = "";
if(typeof(args) !== "undefined") {
  if (args.urls.length > 0) {
    for (let url of args.urls) {
      input_text += "\n- [ ] " + url;
    }
  }
  if (args.fileURLs.length > 0) {
    for (let url of args.fileURLs) {
      input_text += "\n- [ ] " + url;
    }
  }
  if (args.plainTexts.length > 0) {
    for (let url of args.plainTexts) {
      input_text += "\n- [ ] " + url;
    }
  }
}
log(input_text);


async function toread_append(text) {
  var an = new CallbackURL("agenda://x-callback-url/append-to-note");
  an.addParameter("title", title);
  an.addParameter("project-title", project);
  an.addParameter("text", text);
  log(an.getURL());
  var anr = undefined;
  try {
    anr = await an.open();
    log(anr)
  } catch(err) {
    log(err)
    if (!err.includes("The x-callback-url operation was cancelled because you returned to Scriptable")) {
      toread_create(text);
    }
  }
}


async function toread_open(text) {
  var an = new CallbackURL("agenda://x-callback-url/open-note");
  an.addParameter("title", title);
  an.addParameter("project-title", project);
  log(an.getURL());
  var anr = undefined;
  try {
    log("open");
    anr = await an.open();
    log(anr);
  } catch(err) {
    log(err);
    toread_create(text);
  }
}


async function toread_create(text) {
  var cn = new CallbackURL("agenda://x-callback-url/create-note");
  cn.addParameter("title", title);
  cn.addParameter("project-title", project);
  if (typeof text !== 'undefined') {
    cn.addParameter("text", text);
  }
  log(cn.getURL());
  var cnr = undefined;
  try {
    cnr = await cn.open();
    log(cnr)
  } catch(err) {
    log(err)
  }
}

if (input_text == "") {
  toread_open();
} else {
  toread_append(input_text);
}

