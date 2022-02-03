Date.prototype.addDays = function(days) {
  this.setDate(this.getDate() + days);
  return this;
}

var course_dom = document.querySelectorAll("tbody tr.ant-table-row")

var course_result = []

course_dom.forEach(function(course_) {
  const course = course_.querySelectorAll("td")
  const dts = dt_convert(course[7].innerText.split('-')[0])

  var course_name = course[4].innerText
  var course_location = course[7].innerText.split('-')[1]

  dts.forEach(function(course_dt) {
    var school_start_date = new Date("14 Feb 2022 00:00 UTC")
    
    date_ = school_start_date.addDays(course_dt['weekday'] - 1).toISOString().substring(0,11).replaceAll('-', '')

    start_dt = date_ + course_dt['time']['start']
    end_dt = date_ + course_dt['time']['end']

    course_result.push({
      title: course_name, 
      start_dt: start_dt, 
      end_dt: end_dt, 
      location: course_location
    })

  })
  
})

console.log(generate_ics(course_result))

function dt_convert(time_str) {
  const weekday_table = {
    M: 1,
    T: 2,
    W: 3,
    R: 4,
    F: 5,
    S: 6,
    U: 7
  }

  var time_re = /([MTWRFSU])([123456789abcdyzn]*)/g
  var time_ = [...time_str.matchAll(time_re)]
  var result = []

  time_.forEach(function(time) {
    var result_ = {
      weekday: weekday_table[time[1]],
      time: time_convert(time[2])
    }

    result.push(result_)
  })

  return result
}

// 56
function time_convert(time_str) {
  const time_table = {
    y: ['060000', '065000'],
    z: ['070000', '075000'],
    2: ['090000', '095000'],
    1: ['080000', '085000'],
    3: ['101000', '110000'],
    4: ['111000', '120000'],
    n: ['122000', '131000'],
    5: ['132000', '141000'],
    6: ['142000', '151000'],
    7: ['153000', '162000'],
    8: ['163000', '172000'],
    9: ['173000', '182000'],
    a: ['183000', '192000'],
    b: ['193000', '202000'],
    c: ['203000', '212000'],
    d: ['213000', '222000']
  }
  var time_result = {
    start: null,
    end: null
  }
  for (var i=0; i<time_str.length;i++) {
    

    if(i == 0) {
      time_result['start'] = time_table[time_str[i]][0]
    }

    if(i == time_str.length - 1) {
      time_result['end'] = time_table[time_str[i]][1]
    }
  }

  return time_result

}

function new_event( title, start_dt, end_dt, location ) {
  return (
    "BEGIN:VEVENT\n" +
    "UID:" + performance.now().toString() + ".nycu." + Math.random().toString() + "\n" +
    "DTSTART;TZID=Asia/Taipei:" + start_dt + "\n" +
    "DTEND;TZID=Asia/Taipei:" + end_dt + "\n" +
    "SUMMARY:" + title + "\n" +
    "LOCATION:" + location + "\n" + 
    "END:VEVENT\n"
  )
}

function generate_ics(events_) {
  var ics_template = "BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nPRODID:-//Test Cal//EN\nVERSION:2.0\n{events}END:VCALENDAR"
  var events = []

  events_.forEach(function(event) {
    events.push(new_event(event['title'], event['start_dt'], event['end_dt'], event['location']))
  })

  return ics_template.replace('{events}', events.join(""))
}
