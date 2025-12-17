/* Global Variables */
const dayNames = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
const dayNamesFull = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
const monthNames = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
const milongaCalendar = document.getElementById("cal")
let defaultAmount = 0;
if(screen.width <= 600){defaultAmount = 2}else{defaultAmount = 5}; // Set this dynamically with regard to the screen width. Mobile 2, Desktop 5
let milongas = []
let lastMilongaInCurrentCal = -1 // index of milongas
let currentMonth = -1 // Will be a Date object once first milongas has been displayed

async function initMilongaCal(){
    milongas = await getMilongas()
    milongas = processMilongas(milongas)
    displayNextMilongas(defaultAmount)
}


async function getMilongas(){
  const url = "./data/milongas.json";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error.message);

    const calContainer = document.getElementById('cal');
    if (calContainer) {
        calContainer.innerHTML = `
            <div role="alert" class="error-message">
                <p>
                    <strong>Fehler beim Laden der Milongas.</strong><br>
                    Bitte versuche es später erneut oder kontaktiere mich.
                </p>
            </div>
        `;
    }
    return [];
  }
}

function displayNextMilongas(k){
/**
 * Displays the next k milongas in the calendar. If less than k milongas are yet to be displayed, will display all remaining ones instead.
 * Checks if new month divider is needed and calls {@link createMonthDivider(date)}} function to create it.
 * 
 * 
 * @param {number} k – The number of milongas to display
 * */
    // Sanity check
    if (k > milongas.length){
        k = milongas.length;
    }

    // For the next k milongas check
    const goalIndex = lastMilongaInCurrentCal + k
    let html_buffer = ''
    const oldIndex = lastMilongaInCurrentCal

    while (lastMilongaInCurrentCal < goalIndex) {
        const nextMilonga = lastMilongaInCurrentCal + 1
        const nextDate = milongas[nextMilonga].date
        const nextMonth = nextDate.getMonth()
        // Check if the current milonga is in a new month. Will also work in the Dec -> Jan case.
        if(nextMonth != currentMonth){
            html_buffer += createMonthDividerHTML(nextDate)
            currentMonth = nextMonth
        }
        html_buffer += createMilongaHTML(milongas[nextMilonga])
        lastMilongaInCurrentCal +=1
    }

    milongaCalendar.insertAdjacentHTML('beforeend', html_buffer)

    // Announce to screen readers how many milongas were loaded
    const addedCount = lastMilongaInCurrentCal - oldIndex
    announceUpdate(addedCount)
}


function announceUpdate(count) {
    /**
     * Announces to screen readers that new milongas have been loaded.
     * Creates a temporary status message that is automatically cleared after 3 seconds.
     *
     * @param {number} count - The number of milongas that were loaded
     */
    const statusElement = document.getElementById('status-message');
    if (statusElement) {
        statusElement.textContent = `${count} weitere Milongas geladen`;
        // Clear message after 5 seconds to avoid repeated announcements
        setTimeout(() => {
            statusElement.textContent = '';
        }, 5000);
    }
}


function collapseMilongas(){
    /**
     * Deletes all milongas and month-divider leaving only the default amount.
     */
    while(lastMilongaInCurrentCal > defaultAmount -1){
        let lastEntry = milongaCalendar.lastChild
        // Check if last entry is a month divider
        if (lastEntry.className === "month-divider")
            {lastEntry.remove()
            lastEntry = milongaCalendar.lastChild
            }
        lastEntry.remove()
        lastMilongaInCurrentCal -= 1;
    }

    // Edge case where one last month-divier is not removed because while-loop ended when defaultAmount was reached. 
    if (milongaCalendar.lastChild.className === "month-divider")
        {milongaCalendar.lastChild.remove()}
    
    // Reset current month so calling displayNextMilongas will work
    currentMonth = milongas[lastMilongaInCurrentCal].date.getMonth()
}


function createMonthDividerHTML(date){
    /**
 * Creates a month divider HTML for a given date.
 *
 * @param {Date} – A Date Object.
 * */
    const divider = monthNames[date.getMonth()] + " " + date.getFullYear()
    html = `<h3 class = "month-divider">${divider}</h3>`;

    return html
}


function processMilongas(milongas){
/**
 * Converts date string to date object, then sorts by date and filters for all milongas now and in the future
 * 
 * @param {json} milonga – One list element in JSON format containing information about the milonga
 * @returns {Array[JSON]} – An array whose elements are milongas in JSON format 
 * */
    // Convert date string to Date object
    milongas.forEach(element => element.date = new Date(element.date))
    // Sort by date
    milongas.sort((a,b) => {return a.date - b.date});
    // Return milongas that are today or later
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    return milongas.filter(element => element.date >= today)
}


function createMilongaHTML(milonga){
/**
 * Displays a given milonga at the end of the current calendar.
 * 
 * @param {json} milonga – One list element in JSON format containing information about the milonga
 * @returns – None 
 * */

    // Get all data and format if necessary
    const weekday = dayNames[milonga.date.getDay()]
    const weekdayFull = dayNamesFull[milonga.date.getDay()]
    const date = milonga.date.getDate();
    const year = milonga.date.getFullYear();
    const month = monthNames[milonga.date.getMonth()]
    const time = milonga.start_time + " bis " + milonga.end_time + " Uhr";
    const title = milonga.title;
    const venue = milonga.venue + ", ";
    const street = milonga.street + "\u00A0" + milonga.house_number + ", ";
    const city = milonga.postal_code + "\u00A0" + milonga.city;
    const dj = milonga.dj;
    const dj_style = milonga.style;
    const description = milonga.description;
    const isoDate = milonga.date.toISOString().split('T')[0];

    html =
        `<li>
            <article class = "milonga" tabindex="0" 
            aria-label="${weekdayFull}, ${date} ${month} ${year}: ${title}. Von ${time}. Musik von ${dj}. Der Stil der Musik ist: ${dj_style}.
            Veranstaltungsort: ${venue} ${street} ${city}">
                <time class = "milonga-date" style = "grid-area: day" datetime="${isoDate}">
                    <div class = "weekday" style = "grid-area: day" aria-label="${weekdayFull}">${weekday}</div>
                    <div class = "date">${date}</div>
                </time>
                <time class = "milonga-time" style = "grid-area: time">${time}</time>
                <h4 class = "milonga-title" style = "grid-area: title">${title}</h4>
                <address class = "milonga-location" style = "grid-area: location">
                    <span class = "venue">${venue}</span>
                    <span class = "street">${street}</span>
                    <span class = "city">${city}</span>
                </address>
                <div class = "milonga-dj" style = "grid-area: dj" aria-label="DJ: ${dj}">
                    <div class = "dj-name">${dj}</div>
                    <div class = "dj-style" style = "grid-area: style">${dj_style}</div>
                </div>`
        if(description != null){
            html += 
        `<aside class = "milonga-description" role ="note" style="grid-area: desc"><span class = "anmerkung">Anmerkung</span>: ${description}</aside>`
        }
        html += `
            </article>
        </li>`;

    return html;
}

// Buttons
const moreBtn = document.getElementById("show-more")
const lessBtn =  document.getElementById("show-less")
moreBtn.onclick = () => {
    displayNextMilongas(defaultAmount);
    lessBtn.style.display = "flex";
}
lessBtn.onclick = () => {
    collapseMilongas()
    {lessBtn.style.display = "none";}
    lessBtn.style.display = "none";
}


function generateAllMilongaSchemas(){
/**
 * Generates Schema.org DanceEvent JSON-LD markup for all milongas and injects it into the document head.
 * Called after milongas data has been loaded and processed.
 * SEO: Helps Google display events in rich search results and Google Event Search.
 */
    milongas.forEach(milonga => {
        // Build the schema object
        const schema = {
            "@context": "https://schema.org",
            "@type": "DanceEvent",
            "name": milonga.title,
            "startDate": milonga.date.toISOString().split('T')[0] + 'T' + milonga.start_time,
            "endDate": milonga.date.toISOString().split('T')[0] + 'T' + milonga.end_time,
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {
                "@type": "Place",
                "name": milonga.venue,
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": milonga.street + " " + milonga.house_number,
                    "addressLocality": milonga.city,
                    "postalCode": milonga.postal_code,
                    "addressCountry": "DE"
                }
            },
            "performer": {
                "@type": "Person",
                "name": milonga.dj
            }
        }

        // Add optional fields only if they exist and are not null
        if (milonga.description) {
            schema.description = milonga.description
        }

        if (milonga.url) {
            schema.url = milonga.url
        }

        if (milonga.organizer) {
            schema.organizer = {
                "@type": "Organization",
                "name": milonga.organizer
            }
            if (milonga.organizer_url) {
                schema.organizer.url = milonga.organizer_url
            }
        }

        if (milonga.price !== null) {
            schema.offers = {
                "@type": "Offer",
                "price": milonga.price,
                "priceCurrency": milonga.currency,
                "availability": "https://schema.org/InStock",
                "url": milonga.url || "https://tangotübingen.de/"
            }
        }

        // Create script element and inject into head
        const script = document.createElement('script')
        script.type = 'application/ld+json'
        script.text = JSON.stringify(schema)
        document.head.appendChild(script)
    })
}