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
  Button,
  Stack,
  Snackbar,
  Alert,
} from "@mui/material";

function App() {
  const [events, setEvents] = useState([]);
  const [users, setUsers] = useState([]);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "info",
  });

  // Load events and users
  useEffect(() => {
    axios
      .get("http://localhost:5000/events")
      .then((res) => {
        console.log("📅 Events:", res.data);
        setEvents(res.data);
      })
      .catch((err) => console.error("❌ Events fetch error:", err));

    axios
      .get("http://localhost:5000/users")
      .then((res) => {
        console.log("👤 Users:", res.data);
        setUsers(res.data);
      })
      .catch((err) => console.error("❌ Users fetch error:", err));
  }, []);

  const startCamera = async () => {
    try {
      const response = await axios.post("http://localhost:4000/start-camera");
      const status = response.status;

      setSnackbar({
        open: true,
        message: response.data.message,
        severity: status === 200 ? "success" : "warning", // 200 OK or 409 Conflict
      });
    } catch (error) {
      const fallbackMsg =
        error.response?.data?.error || "Failed to start camera ❌";
      const status = error.response?.status;

      setSnackbar({
        open: true,
        message: error.response?.data?.message || fallbackMsg,
        severity: status === 409 ? "warning" : "error",
      });
    }
  };

  const stopCamera = async () => {
    try {
      const response = await axios.post("http://localhost:4000/stop-camera");
      const status = response.status;

      setSnackbar({
        open: true,
        message: response.data.message,
        severity: status === 200 ? "success" : "warning",
      });
    } catch (error) {
      const fallbackMsg =
        error.response?.data?.error || "Failed to stop camera ❌";
      const status = error.response?.status;

      setSnackbar({
        open: true,
        message: error.response?.data?.message || fallbackMsg,
        severity: status === 409 ? "warning" : "error",
      });
    }
  };

  return (
    <Container>
      <Typography variant="h3" gutterBottom>
        Events Dashboard
      </Typography>

      <Stack direction="row" spacing={2} mb={3}>
        <Button variant="contained" color="success" onClick={startCamera}>
          Start Camera Client
        </Button>
        <Button variant="contained" color="error" onClick={stopCamera}>
          Stop Camera Client
        </Button>
      </Stack>

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
                  {event.participants.map((id) => {
                    const user = users.find((u) => u._id === id);
                    return user ? (
                      <p key={id}>
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

      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          severity={snackbar.severity}
          variant="filled"
          onClose={() => setSnackbar({ ...snackbar, open: false })}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default App;
