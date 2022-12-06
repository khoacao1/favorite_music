import './App.css';
import { useState } from 'react';


function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById("data").text);


  function doNothing(e) {
    alert('Input must be field');
    e.preventDefault();
  }

  const [artistids, setArtistIDs] = useState(args.artist_ids)
  const [artistid, setArtistID] = useState("")

  function addArtistID(e) {
    e.preventDefault();

    setArtistIDs([...artistids, artistid])
    setArtistID("")
  }

  function deleteartist(id) {
    const updatedArtistids = [...artistids].filter((artistid) => artistid !== id)

    setArtistIDs(updatedArtistids)
  }

  function saveartist() {
    fetch('/uploadartistid', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ artist_list: artistids }),
    })
      .then((response) => response.json())
      .then((data) => {
        setArtistIDs(data.artistids_server);
        if (data.invalid_count) {
          alert(data.invalid_count + ' artists ID invalid!');
        }
        else {
          alert("Artist's ID data has been saved!")
        }
      });
  }

  // TODO: Implement your main page as a React component.
  return (
    <>
      <h1>{args.nameOfUser}'s Music Wolrd</h1>
      <a href="/logout"><button id="logout">Log Out!</button></a>

      {args.has_artists_saved ?
        (
          <div id="background">
            <div id="infosection">
              <div id="songname">{args.song_name}<br /></div>
              <div id="artist"><span>Artist -</span>
                <a href={args.artist_url}>{args.artist_name}<br /></a>
              </div>

              <div id="album">
                <span>Album -</span>
                <a href={args.album_url}>{args.album_name}<br /></a>
              </div>
              <img id="album_img" src={args.album_pic_url} alt="" /><br />
              <audio controls id="audio">
                <source src={args.song_preview} />
              </audio><br />
              <a id="spotify_link" href={args.song_url}>Listen full song on Spotify<br /></a>
              <a id="spotify_link" href={args.genius}>Lyric<br /></a>
            </div>
          </div>
        )
        :
        (
          <div id="errormessage">
            No Artist's ID or Something went wrong. Please try again...
          </div>
        )
      }
      <div>
        <table>
          {artistids.map(function (artistID, index) {
            return (
              <tr>
                <td key={index}>{artistID}</td>
                <td>
                  <button id="deletebutton" onClick={() => deleteartist(artistID)} >Delete</button>
                </td>
              </tr>
            );
          })}
        </table>
        <button type="button" id="save" onClick={saveartist}>Save</button>
        <form onSubmit={artistid ? addArtistID : doNothing} >
          <input type="text" onChange={(e) => setArtistID(e.target.value)} value={artistid} />
          <button id="button" type="submit">Add Aritst ID</button>
        </form>
      </div>
    </>
  );
}
export default App;
