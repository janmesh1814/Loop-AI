import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  Paper,
  Box
} from "@mui/material";
import { Order } from "../types";

interface Props {
  orders: Order[];
}

const statusColor = (status: Order["status"]) => {
  if (status === "completed") return "success";
  if (status === "failed") return "error";
  if (status === "processing") return "warning";
  return "default";
};

export function OrdersTable({ orders }: Props) {
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
          ml:3
        }}
      >
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order ID</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Items</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {orders.map(order => (
              <TableRow key={order.id}>
                <TableCell>{order.id}</TableCell>
                <TableCell>
                  <Chip
                    label={order.status}
                    color={statusColor(order.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  ${Number(order.total_amount).toFixed(2)}
                </TableCell>
                <TableCell>{order.items_count}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Box>
  );
}
