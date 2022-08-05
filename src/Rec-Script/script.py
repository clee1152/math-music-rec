import spotify_to_csv as stc
import recommender as r
import sys

def main():
    args = sys.argv[1:]
    if len(args) != 3:
        print("usage: python3 script.py <playlist_id> <popularity> <num_recommendations>")
        return

    CLIENT_ID     = ###   CLIENT_ID   ###
    CLIENT_SECRET = ### CLIENT_SECRET ###
    REDIRECT_URI  = ###  REDIRECT_URI ###
    PLAYLIST_ID   = args[0]
    stc.spotify_to_csv(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, PLAYLIST_ID)
    r.filter_tracks(int(args[1]))
    num_recs, recommendations = r.get_recommendations(int(args[2]))
    r.print_recs(recommendations, int(args[1]), num_recs)
    
if __name__ == '__main__':
    main()
