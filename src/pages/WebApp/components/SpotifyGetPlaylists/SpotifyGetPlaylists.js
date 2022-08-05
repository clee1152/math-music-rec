import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PLAYLISTS_ENDPOINT = 'https://api.spotify.com/v1/me/playlists';

const SpotifyGetPlaylists = () => {
    const [token, setToken] = useState('');
    const [data, setData] = useState({});

    useEffect(() => {
        if (localStorage.getItem('accessToken')) {
            setToken(localStorage.getItem('accessToken'));
        };
    }, []);

    const handleGetPlaylists = () => {
        axios
        .get(PLAYLISTS_ENDPOINT, {
            headers: {
                Authorization: 'Bearer ' + token,
            }
        }).then(response => {
            setData(response.data);
        })
        .catch((error) => {
            console.log(error);
        });
    };
    console.log(data);
    return (
        <>
            <button onClick={handleGetPlaylists}>Get Playlists</button>
            <ol>
                {data.items ? data.items.map((item) => 
                <li key={item.name}>
                        Name: {item.name} ID: {item.id}
                </li>) : null} 
            </ol>
            
        </>
    );
    
};

export default SpotifyGetPlaylists;