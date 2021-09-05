const port = 3000;

const mysql = require('mysql');
const express = require('express');
const csv = require('fast-csv');
const fs = require('fs');
const axios = require('axios');
const cookieParser = require("cookie-parser");

const connection = mysql.createConnection({
    host     : 'mysql',
    user     : 'root',
    password : 'root',
    database : 'dataset'
});
connection.connect(function(err) {
    if (err) {
        return console.error('error connecting: ' + err.stack);
    }
    console.log('connected as id ' + connection.threadId);
    app.listen(port,()=>{
        console.log(`listening on ${port}`)
    })
});

const app = express();
app.use(cookieParser());


app.set('view engine', 'ejs');
app.use('/static', express.static('static'));

app.get('/cart', (req, res) => {
    const cartIds = JSON.parse(req.cookies.cart).join(",");
    connection.query(`SELECT * FROM dataset_new WHERE \`Идентификатор СТЕ\` IN (${cartIds});`,
        async function (error, cart, fields) {
            if (error && cart.length !== 0) throw error;
            connection.query(`
SELECT * FROM dataset_new WHERE 
(\`Категория\` IN (${cart.map(item=>'\''+item['Категория']+'\'').join(",")}) AND \`Идентификатор СТЕ\` NOT IN (${cartIds})) 
ORDER BY \`Просмотры\` DESC LIMIT 4`,
                async function (error, results, fields) {
                    if (error && cart.length !== 0) throw error;
                    res.render("cart", {
                        items: await Promise.all(addImages(cartIds.length !== 0 ? cart : [])),
                        recommended: await Promise.all(addImages(cartIds.length !== 0 ? results : []))
                    });
                });
        });


})
app.get('/item/:id', async (req, res) => {
    const id = req.params.id;
    connection.query(`SELECT * FROM dataset_new WHERE \`Идентификатор СТЕ\` = ${id};`,
        async function (error, results, fields) {
            if (error) throw error;
            console.log(results);
            connection.query(`SELECT * FROM dataset_new WHERE 
(\`Категория\`= '${results[0]['Категория']}' AND \`Идентификатор СТЕ\` <> ${id}) 
ORDER BY \`Просмотры\` DESC LIMIT 4`,
                async function (error, recommendations, fields) {
                    if (error) throw error;
                    const recommended = await Promise.all(addImages(recommendations));
                    res.render("item", {
                        item: await addImages(results)[0],
                        recommended
                    });
                });
        });

    // const info = await axios.get(`https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity?id=${id}`);
    // res.render("item", {
    //     item: {...items[id], image: '/static/image.svg'},
    //     recommended: await Promise.all(addImages(sorted.map(id=>items[id])
    //         .filter(i=>i.category === items[id].category).slice(0, 3)))
    // });
})

app.get('/', async (req, res) => {
    connection.query(`SELECT * FROM dataset_new ORDER BY \`Просмотры\` DESC LIMIT 12`,
        async function (error, results, fields) {
            if (error) throw error;
            console.log(results);
            res.render("catalog", {items: await Promise.all(addImages(results))});
        });

})


function addImages(items) {
    return items.map(async item => {
        const info = await axios
            .get(`https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity?id=${item['Идентификатор СТЕ']}`);
        return {
            ...item,
            image: `https://zakupki.mos.ru/newapi/api/Core/Thumbnail/${info.data.images[0].fileStorage.id}/300/300`
        };
    });
}