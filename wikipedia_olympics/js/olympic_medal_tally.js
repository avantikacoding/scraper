const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const crypto = require('crypto');

async function scrapeOlympicsMedalTally (url){
    const headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    };
    try{
        const response = await axios.get(url, { headers });
        if (response.status === 200) {
            const $ = cheerio.load(response.data);
            const table = $('.wikitable.sortable.plainrowheaders.jquery-tablesorter')
            // console.log($.html())
            // console.log(table.html())

            if(table.length <= 0){
                console.log('Table not found on the page.');
                return [];
            }
            const medalTally = []


            const rowIndex = table.find('tr').slice(1,-1)

            // console.log(rowIndex,'rowIndex')

            rankedRowIndex =-1;
            
            rowIndex.each((index, element) => {
                const cells = $(element).find('th, td');

                if (cells.length >= 6) {
                    rankedRow = index+1;
                    const countryName = cells.eq(1).text().trim().toLowerCase().replace(/\s/g, '');
                    const hash = crypto.createHash('sha256').update(countryName).digest('hex');
                    const id = hash;
                    const rank = cells.eq(0).text().trim();
                    const country = cells.eq(1).text().trim();
                    const gold = cells.eq(2).text().trim();
                    const silver = cells.eq(3).text().trim();
                    const bronze = cells.eq(4).text().trim();
                    const total = cells.eq(5).text().trim();

                    medalTally.push({
                        'countryHash' : id,
                        'Country': country,
                        'Rank': rank,
                        'Gold': gold,
                        'Silver': silver,
                        'Bronze': bronze,
                        'Total': total
                    });
                } else if (cells.length === 5) {
                    const countryName = cells.eq(1).text().trim().toLowerCase().replace(/\s/g, '');
                    const hash = crypto.createHash('sha256').update(countryName).digest('hex');
                    const id = hash;
                    const lastRow = table.find('tr').eq(rankedRow).find('th, td');
                    const rank = lastRow.eq(0).text().trim();
                    const country = cells.eq(0).text().trim();
                    const gold = cells.eq(1).text().trim();
                    const silver = cells.eq(2).text().trim();
                    const bronze = cells.eq(3).text().trim();
                    const total = cells.eq(4).text().trim();
    
                    medalTally.push({
                        'countryHash' : id,
                        'Country': country,
                        'Rank': rank,
                        'Gold': gold,
                        'Silver': silver,
                        'Bronze': bronze,
                        'Total': total
                    });
                }

                
            })
            return medalTally;


        } else {
            console.log("Failed to retrieve the web page. Status code:", response.status);
            return [];
        }
    }
    catch (error){ 
        console.error("An error occurred:", error);
    };

}

const url = 'https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table';

// Calling createHash method


scrapeOlympicsMedalTally(url).then((medalTally) => {

    const json = JSON.stringify(medalTally, null, 4);
    fs.writeFileSync('MedalTally.json', json);
}).catch((error) => {
    console.error('Error:', error);
});



/* -------------------------------------------------------------------------- */
/*                  // Polling to see if the ip gets blocked                  */
/* -------------------------------------------------------------------------- */
// Helper function to delay execution
// const delay = ms => new Promise(resolve => setTimeout(resolve, ms));


// async function runScrape() {
//     for (let i = 0; i < 10; i++) {  // Example limit to avoid indefinite loop
//         console.log(`Scrape attempt ${i+1}`);
//         await scrapeOlympicsMedalTally(url).then((medalTally) => {
//             const json = JSON.stringify(medalTally, null, 4);
//             fs.writeFileSync(`MedalTally.json`, json);
//         }).catch((error) => {
//             console.error('Error:', error);
//         });
//         await delay(2000);  
//     }
// }

// runScrape();