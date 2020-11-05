import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import TextField from "@material-ui/core/TextField";

const drawerWidth = 200;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    textTransform: "capitalize",
    color: "red",
  },
  drawerPaper: {
    width: drawerWidth,
  },
  // necessary for content to be below app bar
  toolbar: {
    minHeight: "75px",
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  searchTags: {
    "& > *": {
      margin: theme.spacing(1),
      width: "160px",
    },
  },
}));

function SideBar(props) {
  const classes = useStyles();
  console.log(props.tags);
  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
      anchor="left"
    >
      {/* <form className={classes.searchTags} noValidate autoComplete="off">
        <TextField id="outlined-basic" label="Search Tags" variant="outlined" />
      </form> */}
      <div className={classes.toolbar} />
      <Divider />
      <List>
        {props.tags
          .map((o) => o.name)
          .map((text, index) => (
            <>
              <ListItem button key={text}>
                <ListItemText primary={text} />
              </ListItem>
              <Divider />
            </>
          ))}
      </List>
    </Drawer>
  );
}

export default SideBar;
