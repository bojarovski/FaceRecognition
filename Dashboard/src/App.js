import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Button, // Import Button component
} from "@mui/material";

function App() {
  const [events, setEvents] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/events")
      .then((response) => setEvents(response.data))
      .catch((error) => console.log("Error fetching events:", error));

    axios
      .get("http://localhost:5000/users")
      .then((response) => setUsers(response.data))
      .catch((error) => console.log("Error fetching users:", error));
  }, []);

  const startCamera = () => {
    axios
      .post("http://localhost:4000/start-camera")
      .then((response) => {
        alert("Camera client started successfully!");
      })
      .catch((error) => {
        console.error("Error starting the camera client:", error);
        alert("Failed to start the camera client.");
      });
  };

  return (
    <Container>
      <Typography variant="h3" gutterBottom>
        Events Dashboard
      </Typography>

      {/* Add Button for starting the camera client */}
      <Button variant="contained" color="primary" onClick={startCamera}>
        Start Camera Client
      </Button>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Event Name</TableCell>
              <TableCell>Start Time</TableCell>
              <TableCell>End Time</TableCell>
              <TableCell>Participants</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {events.map((event) => (
              <TableRow key={event._id}>
                <TableCell>{event.name}</TableCell>
                <TableCell>
                  {new Date(event.startTime).toLocaleString()}
                </TableCell>
                <TableCell>
                  {new Date(event.endTime).toLocaleString()}
                </TableCell>
                <TableCell>
                  {event.participants.map((userId) => {
                    const user = users.find((user) => user._id === userId);
                    return user ? (
                      <p key={userId}>
                        {user.name} {user.surname}
                      </p>
                    ) : null;
                  })}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default App;
