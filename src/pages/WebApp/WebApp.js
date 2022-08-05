import React, { useEffect } from 'react';
import SpotifyGetPlaylists from './components/SpotifyGetPlaylists/SpotifyGetPlaylists';
import './WebApp.css';

const CLIENT_ID = '554c37e7400b415ebdf65b6446b4287b';
const SPOTIFY_AUTHORIZE_ENDPOINT = 'https://accounts.spotify.com/authorize';
const REDIRECT_URI_AFTER_LOGIN = 'http://localhost:3000';
const SPACE_DELIMITER = '%20';
const SCOPES = [];
const SCOPES_URL_PARAM = SCOPES.join(SPACE_DELIMITER);

const getReturnedParamsFromSpotifyAuth = (hash) => {
    const stringAfterHashTag = hash.substring(1);
    const paramsInUrl = stringAfterHashTag.split('&');
    const paramsSplitUp = paramsInUrl.reduce((accumulater, currentValue) => {
        const [key, value] = currentValue.split('=');
        accumulater[key] = value;
        return accumulater;
    }, {});

    return paramsSplitUp;
};

const WebApp = () => {
    useEffect(() => {
        if (window.location.hash) {
            const {access_token, 
                expires_in, 
                token_type
            } = getReturnedParamsFromSpotifyAuth(window.location.hash);

            localStorage.clear();
            localStorage.setItem('accessToken', access_token);
            localStorage.setItem('tokenType', token_type);
            localStorage.setItem('expiresIn', expires_in);
        }
    });

    const handleLogin = () => {
        window.location = `${SPOTIFY_AUTHORIZE_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI_AFTER_LOGIN}&scope=${SCOPES_URL_PARAM}&response_type=token&show_dialog=true`;
    };
    return <div className='container'>
        <h1>Mathematical Music Recommender</h1>
        <button onClick={handleLogin}>Login to Spotify</button>
        <SpotifyGetPlaylists />
    </div>;
};

export default WebApp;