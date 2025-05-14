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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

export default function App() {
  // ───────────────── state ─────────────────
  const [events, setEvents] = useState([]);
  const [attendance, setAttendance] = useState({}); // { [eventId]: [ { user, seenAt } ] }
  const [currentEvent, setCurrentEvent] = useState(null); // for camera

  const [dialogOpen, setDialogOpen] = useState(false);
  const [eventName, setEventName] = useState("");

  const [attendeesOpen, setAttendeesOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "info",
  });

  // ───────────────── helpers ─────────────────
  const notify = (message, severity = "info") =>
    setSnackbar({ open: true, message, severity });

  const refreshEvents = async () => {
    try {
      const { data } = await axios.get("http://localhost:5050/events");
      setEvents(data);
    } catch (err) {
      console.error(err);
      notify("Failed to load events", "error");
    }
  };

  const fetchAttendance = async (eventId) => {
    try {
      const { data } = await axios.get(
        `http://localhost:5050/attendance/event/${eventId}`
      );
      setAttendance((prev) => ({ ...prev, [eventId]: data }));
    } catch (err) {
      console.error(err);
    }
  };

  const startCamera = async (eventId) => {
    try {
      const { data, status } = await axios.post(
        "http://localhost:4000/start-camera",
        { eventId }
      );
      notify(data.message, status === 200 ? "success" : "warning");
    } catch (err) {
      const status = err.response?.status;
      const msg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Failed to start camera";
      notify(msg, status === 409 ? "warning" : "error");
    }
  };

  const stopCamera = async () => {
    try {
      const { data, status } = await axios.post(
        "http://localhost:4000/stop-camera"
      );
      notify(data.message, status === 200 ? "success" : "warning");
    } catch (err) {
      const status = err.response?.status;
      const msg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Failed to stop camera";
      notify(msg, status === 409 ? "warning" : "error");
    }
  };

  // ───────────────── lifecycle ─────────────────
  useEffect(() => {
    refreshEvents();
  }, []);

  useEffect(() => {
    events.forEach((e) => fetchAttendance(e._id));
  }, [events]);

  // ───────────────── camera flow ─────────────────
  const handleStartClick = () => {
    setDialogOpen(true);
  };

  const handleConfirmStart = async () => {
    if (!eventName.trim()) {
      notify("Please enter an event name", "warning");
      return;
    }

    try {
      const { data: newEvent } = await axios.post(
        "http://localhost:5050/events",
        {
          name: eventName,
          startTime: new Date().toISOString(),
          endTime: new Date().toISOString(),
        }
      );
      setCurrentEvent(newEvent);
      await refreshEvents();
      await startCamera(newEvent._id);
      setDialogOpen(false);
      setEventName("");
    } catch (err) {
      console.error(err);
      notify("Failed to start event", "error");
    }
  };

  const handleDeleteEvent = async (eventId) => {
    if (!window.confirm("Are you sure you want to delete this event?")) return;
    try {
      await axios.delete(`http://localhost:5050/events/${eventId}`);
      notify("Event deleted", "info");
      // refresh both lists
      refreshEvents();
      setAttendance((a) => {
        const { [eventId]: _, ...rest } = a;
        return rest;
      });
    } catch (err) {
      console.error(err);
      notify("Failed to delete event", "error");
    }
  };

  const handleStopClick = async () => {
    if (!currentEvent) return;
    try {
      await stopCamera();
      await axios.patch(
        `http://localhost:5050/events/${currentEvent._id}/close`
      );
      await refreshEvents();
      await fetchAttendance(currentEvent._id);
    } catch (err) {
      console.error(err);
      notify("Failed to stop event", "error");
    } finally {
      setCurrentEvent(null);
    }
  };

  // ───────────────── attendees dialog ─────────────────
  const handleViewAttendees = (event) => {
    setSelectedEvent(event);
    if (!attendance[event._id]) fetchAttendance(event._id);
    setAttendeesOpen(true);
  };

  const handleCloseAttendees = () => {
    setAttendeesOpen(false);
    setSelectedEvent(null);
  };

  // ───────────────── rendering ─────────────────
  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom>
        Events Dashboard
      </Typography>

      <Stack direction="row" spacing={2} mb={3}>
        <Button
          variant="contained"
          color="success"
          onClick={handleStartClick}
          disabled={!!currentEvent}
        >
          Start Camera Client
        </Button>
        <Button
          variant="contained"
          color="error"
          onClick={handleStopClick}
          disabled={!currentEvent}
        >
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
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {events.map((event) => {
              const rows = attendance[event._id] || [];
              return (
                <TableRow key={event._id}>
                  <TableCell>{event.name}</TableCell>
                  <TableCell>
                    {new Date(event.startTime).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    {new Date(event.endTime).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    {rows.length === 0 ? "—" : `${rows.length}`}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleViewAttendees(event)}
                      sx={{ mr: 1 }}
                    >
                      View Attendees
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      size="small"
                      onClick={() => handleDeleteEvent(event._id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Attendees Dialog */}
      <Dialog open={attendeesOpen} onClose={handleCloseAttendees} fullWidth>
        <DialogTitle>Attendees for {selectedEvent?.name || ""}</DialogTitle>
        <DialogContent dividers>
          <List>
            {(attendance[selectedEvent?._id] || []).map(({ user }) => (
              <ListItem key={user._id} divider>
                <ListItemText
                  primary={`${user.name} ${user.surname}`}
                  secondary={new Date(user.seenAt).toLocaleString()}
                />
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAttendees}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Event-name prompt */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Enter new event name</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Event Name"
            fullWidth
            value={eventName}
            onChange={(e) => setEventName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleConfirmStart}>
            Start
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={() => setSnackbar((s) => ({ ...s, open: false }))}
      >
        <Alert
          severity={snackbar.severity}
          variant="filled"
          onClose={() => setSnackbar((s) => ({ ...s, open: false }))}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}
