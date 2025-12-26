import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Box,
  Chip
} from "@mui/material";
import { Store } from "../types";

interface Props {
  stores: Store[];
  onSelect: (store: Store) => void;
}

const statusColor = (status: Store["status"]) => {
  if (status === "online") return "success";
  if (status === "busy") return "warning";
  return "default";
};

export function StoreList({ stores, onSelect }: Props) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        width: "100%",
        mt: 2
      }}
    >
      <Paper
        elevation={3}
        sx={{
          width: "100%",
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Store Name</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Platform</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>City</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {stores.map(store => (
              <TableRow
                key={store.id}
                hover
                onClick={() => onSelect(store)}
                sx={{
                  cursor: "pointer",
                  transition: "background-color 0.2s",
                  "&:hover": {
                    backgroundColor: "rgba(25, 118, 210, 0.08)"
                  }
                }}
              >
                <TableCell>{store.name}</TableCell>

                <TableCell>
                  <Chip
                    label={store.platform}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>

                <TableCell>
                  <Chip
                    label={store.status}
                    size="small"
                    color={statusColor(store.status)}
                  />
                </TableCell>

                <TableCell>{store.location.city}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
