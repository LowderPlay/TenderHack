const express = require('express');
const csv = require('fast-csv');
const fs = require('fs');
const axios = require('axios');
const cookieParser = require("cookie-parser");

const app = express();
app.use(cookieParser());

const port = 3000;
const items = [
    // {name: "Ручка шариковая", cost: "10руб.", offers: 1},
    // {name: "Блокнот", cost: "15руб.", offers: 2},
    // {name: "Маркер", cost: "20руб.", offers: 1},
    // {name: "Шапка", cost: "55руб.", offers: 1},
    // {name: "Батарейки AAA", cost: "15руб.", offers: 5},
];
fs.createReadStream('dataset.csv')
    .pipe(csv.parse({ headers: true, delimiter: ';' }))
    .on('error', error => console.error(error))
    .on('data', row => {
        items.push({...row,
            info: JSON.parse(row.info),
            offers: JSON.parse(row.offers).map(o=>o["Name"]),
            price: row.price === "NULL" ? "Нет в наличии" : JSON.parse(row.price)[0]["Cost"]+" руб."
        })
    })
    .on('end', rowCount => console.log(`Parsed ${rowCount} rows`, items));


app.set('view engine', 'ejs');
app.use('/static', express.static('static'));

app.get('/cart', async (req, res) => {
    const cart = JSON.parse(req.cookies.cart).map(i=>i.toString());
    const limited = await Promise.all(addImages(items.filter(i=> cart.includes(i.id))));
    res.render("cart", {
        items: limited,
        recommended: await Promise.all(addImages(items.slice(0, 3)))
    });
})
app.get('/item/:id', async (req, res) => {
    const id = req.params.id;
    if(!items.map(i=>i.id).includes(id)) return res.sendStatus(404);

    const info = await axios.get(`https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity?id=${id}`);
    res.render("item", {
        item: {...items.filter(i => i.id === id)[0], imageId: info.data.images[0].fileStorage.id},
        recommended: await Promise.all(addImages(items.slice(0, 3)))
    });
})

app.get('/', async (req, res) => {
    const limited = await Promise.all(addImages(items.slice(0, 12)))
    res.render("catalog", {items: limited});
})

app.listen(port, () => {
    console.log(`listening at :${port}`);
})

function addImages(items) {
    return items.map(async item => {
        const info = await axios.get(`https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity?id=${item.id}`);
        return {...item, imageId: info.data.images[0].fileStorage.id};
    });
}