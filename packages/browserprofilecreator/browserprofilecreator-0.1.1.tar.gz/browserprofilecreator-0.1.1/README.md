# Browser Profile Creator

Folder-based isolated browser profile generator.

## But why?

Do you really trust your browser to not track you across multiple platforms? Do you really want to be logged-in to any
of the FAANGs all the time? Don't you want to close everything work-related and be done with it?  
Then you need browser profile separation. Simply have a profile for each part of yourself and be sure that _they_ don't
communicate with each other!

The old way to do it manually: https://youtu.be/410_hV1h0yc  
and now it's automated.  

## install

It just needs vanilla python 3

Here a bash-alias for your `.bash_aliases`:  
```bash
alias run-browser-profile-creator="cd /path/to/the/github/browserProfileCreator && python3 main_vanilla.py"
```

Or run it with uvx:
```bash
uvx browserprofilecreator
# or with command line parameters:
uvx --from 'browserprofilecreator[cli]' create --browser chrome --purpose "de-googlify yourself"
```
