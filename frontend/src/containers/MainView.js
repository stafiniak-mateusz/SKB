import React from "react";
import TextField from "@material-ui/core/TextField";
import { withStyles } from "@material-ui/core/styles";
import RequestAPI from "../services/RequestAPI";
import Tiles from "../containers/Tiles";
import SideBar from "../containers/SideBar";

const useStyles = () => ({
  searchTags: {
    "& > *": {
      width: "100%",
      backgroundColor: "white",
    },
    marginLeft: "22px",
    marginRight: "15px",
    paddingTop: "1vh",
    paddingBottom: "1vh",
    minWidth: "32%",
  },
  searchNews: {
    "& > *": {
      width: "100%",
      backgroundColor: "white",
    },

    paddingTop: "1vh",
    paddingBottom: "1vh",
    // marginLeft: "35px",
    // marginRight: "30px",
    minWidth: "64%",
  },
  formsContainer: {
    display: "flex",
  },
});

class MainView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      news: [],
      tags: [],
      tagsSearch: "",
      newsSearch: "",
    };
    this.handleTagSubmit = this.handleTagSubmit.bind(this);
    this.handleNewsSubmit = this.handleNewsSubmit.bind(this);
  }

  componentDidMount() {
    console.log(this.state);
    RequestAPI.get("news", {}).then((data) =>
      this.setState({ news: data.data })
    );
    RequestAPI.get("tag", {}).then((data) =>
      this.setState({ tags: data.data })
    );
  }

  handleNewsSubmit(event) {
    if (event.target.value.includes("&")) {
      alert("Ampersands are not allowed");
    } else {
      RequestAPI.get("news", { title: event.target.value }).then((data) =>
        this.setState({ news: data.data })
      );
    }
    console.log(this.state.news);
  }

  handleTagSubmit(event) {
    if (event.target.value.includes("&")) {
      alert("Ampersands are not allowed");
    } else {
      RequestAPI.get("tag", { name: event.target.value }).then((data) =>
        this.setState({ tags: data.data })
      );
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <div
        style={{
          backgroundColor: "white",
          width: `calc(100vw - 201px)`,
          paddingLeft: "201px",
        }}
      >
        <div className={classes.formsContainer}>
          <form className={classes.searchTags} noValidate autoComplete="off">
            <TextField
              onChange={this.handleTagSubmit}
              id="outlined-basic"
              label="Search Tags"
              variant="outlined"
            />
          </form>
          <form className={classes.searchNews} noValidate autoComplete="off">
            <TextField
              onChange={this.handleNewsSubmit}
              id="outlined-basic"
              label="Search News"
              variant="outlined"
            />
          </form>
        </div>

        <div>
          <SideBar tags={this.state.tags} />
          <Tiles news={this.state.news} />
        </div>
      </div>
    );
  }
}
export default withStyles(useStyles)(MainView);
