let toHours = 3600;
let toDays = toHours*24;
let toWeeks = toDays*7;
let toMonths = toDays*30;
let toYears = toDays*365;

function calculateTime(date) {
    let delta = (new Date() - new Date(date))/1000;

    if (delta/60 < 60) {return `${Math.round(delta/60)} minutes ago`;}
    else if (delta/toHours < 24 ) {return `${Math.round(delta/toHours)} hours ago`}
    else if (delta/toDays < 7) {return `${Math.round(delta/toDays)} days ago`}
    else if (delta/toWeeks < 4) {return `${Math.round(delta/toWeeks)} weeks ago`}
    else if (delta/toDays < 365) {return `${Math.round(delta/toMonths)} months ago`}
    else {return `${Math.round(delta/toYears)} years ago`}
}