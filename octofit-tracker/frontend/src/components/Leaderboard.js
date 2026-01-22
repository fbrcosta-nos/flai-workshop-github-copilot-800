import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard - API Endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(leaderboardData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="container mt-4">
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading leaderboard...</p>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>{error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <h2>🏆 Leaderboard</h2>
      <div className="mb-3">
        <span className="badge bg-warning text-dark">Top Performers</span>
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">User</th>
              <th scope="col">Team</th>
              <th scope="col">Total Points</th>
              <th scope="col">Total Calories</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry.id} className={index < 3 ? 'table-warning' : ''}>
                <td>
                  {index === 0 && <span className="badge badge-rank-1">🥇 1st</span>}
                  {index === 1 && <span className="badge badge-rank-2">🥈 2nd</span>}
                  {index === 2 && <span className="badge badge-rank-3">🥉 3rd</span>}
                  {index > 2 && <span className="badge bg-secondary">{index + 1}</span>}
                </td>
                <td><strong>{entry.user_name || entry.user}</strong></td>
                <td>
                  {entry.team_name || entry.team ? (
                    <span className="badge bg-primary">{entry.team_name || entry.team}</span>
                  ) : (
                    <span className="badge bg-secondary">N/A</span>
                  )}
                </td>
                <td><strong>{entry.total_points}</strong></td>
                <td>{entry.total_calories}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
