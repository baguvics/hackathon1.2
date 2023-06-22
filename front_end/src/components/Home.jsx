import axios from "axios"
import React, { useState } from "react"



const Home = () => {

    const API = 'http://127.0.0.1:8000/api/v1/musor'

    const [value1, setValue1] = useState('')
    const [value2, setValue2] = useState('')

    const functions = async () => {
        const response = await axios.post(API, {
          value1: parseInt(value1),
          value2: parseInt(value2)
        });
        console.log(response.data);
    };

    return(
        <div>
            <br/>
            <input type="text" onChange={(e) => setValue1(parseInt(e.target.value))}></input>
            <br/>
            <input type="text" onChange={(e) => setValue2(parseInt(e.target.value))}></input>
            <br/>
            <button onClick={() => console.log(value1, value2)}>Проверка</button>
            <br/>
            <button onClick={() => functions()}>Клик</button>
        </div>
    );
}

export default Home;